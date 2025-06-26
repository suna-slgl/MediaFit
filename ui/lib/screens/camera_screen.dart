import 'package:flutter/material.dart';
import 'result_screen.dart';

class CameraScreen extends StatelessWidget {
  const CameraScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Canlı Analiz'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            flex: 5,
            child: Container(
              margin: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.black12,
                borderRadius: BorderRadius.circular(16),
              ),
              child: const Center(
                child: Text('Kamera Preview (placeholder)', style: TextStyle(color: Colors.white70)),
              ),
            ),
          ),
          Expanded(
            flex: 2,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Geribildirim göstergesi (ör: renkli çerçeve, simge)
                const Icon(Icons.check_circle, color: Colors.green, size: 48),
                const SizedBox(height: 8),
                const Text('Doğru', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                const SizedBox(height: 24),
                SizedBox(
                  width: 180,
                  child: ElevatedButton(
                    onPressed: () {
                      Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(builder: (_) => const ResultScreen()),
                      );
                    },
                    child: const Text('Egzersizi Bitir'),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
} 