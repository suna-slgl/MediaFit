import 'package:flutter/material.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'result_screen.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  Future<void> startRecord(BuildContext context) async {
    final response = await http.post(Uri.parse('http://192.168.1.101:5000/start_record'));
    print('Start record status: ${response.statusCode}');
    print('Start record body: ${response.body}');
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Egzersiz kaydı başlatıldı (status: ${response.statusCode})')),
    );
  }

  Future<void> stopRecord(BuildContext context) async {
    final response = await http.post(Uri.parse('http://192.168.1.101:5000/stop_record'));
    print('Stop record status: ${response.statusCode}');
    print('Stop record body: ${response.body}');
    if (response.statusCode == 200) {
      try {
        final rapor = json.decode(response.body);
        print('Parsed rapor: $rapor');
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ResultScreen(rapor: rapor),
          ),
        );
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Egzersiz raporu hazırlandı.')),
        );
      } catch (e) {
        print('JSON parse hatası: $e');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Rapor alınamadı: $e')),
        );
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Rapor alınamadı (status: ${response.statusCode})')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF282a36), Color(0xFF1e1f29)],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('Canlı Analiz', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, color: Color(0xFFf8f8f2))),
                    CircleAvatar(
                      radius: 25,
                      backgroundColor: Color(0xFF44475a),
                      child: Icon(Icons.person, color: Color(0xFFf8f8f2), size: 30),
                    ),
                  ],
                ),
                SizedBox(height: 16),
                Expanded(
                  child: Container(
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: Color(0xFF44475a),
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.3),
                          blurRadius: 20,
                          offset: Offset(0, 10),
                        ),
                      ],
                    ),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(24),
                      child: Mjpeg(
                        stream: 'http://192.168.1.101:5000/video_feed',
                        isLive: true,
                        error: (context, error, stack) => Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.error, size: 50, color: Color(0xFF6272a4)),
                              SizedBox(height: 16),
                              Text('Stream yüklenemedi', style: TextStyle(fontSize: 16, color: Color(0xFF6272a4))),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
                SizedBox(height: 20),
                Row(
                  children: [
                    Expanded(
                      child: Container(
                        height: 60,
                        child: ElevatedButton.icon(
                          onPressed: () => startRecord(context),
                          icon: Icon(Icons.play_arrow, size: 28),
                          label: Text('Egzersize Başla', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Color(0xFFbd93f9),
                            foregroundColor: Color(0xFFf8f8f2),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                            elevation: 8,
                          ),
                        ),
                      ),
                    ),
                    SizedBox(width: 16),
                    Expanded(
                      child: Container(
                        height: 60,
                        child: ElevatedButton.icon(
                          onPressed: () => stopRecord(context),
                          icon: Icon(Icons.stop, size: 28),
                          label: Text('Bitir', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Color(0xFFff5555),
                            foregroundColor: Color(0xFFf8f8f2),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                            elevation: 8,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
} 