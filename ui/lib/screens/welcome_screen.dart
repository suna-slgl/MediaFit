import 'package:flutter/material.dart';
import 'home_screen.dart';
// import 'home_screen.dart'; // HomeScreen oluşturulunca açılacak

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

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
                SizedBox(height: 40),
                Text(
                  'MediaFit',
                  style: TextStyle(
                    fontSize: 40,
                    fontWeight: FontWeight.w900,
                    color: Color(0xFFf8f8f2),
                  ),
                ),
                SizedBox(height: 8),
                Text(
                  'AI Destekli Egzersiz Uygulaması',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    color: Color(0xFF6272a4),
                  ),
                ),
                SizedBox(height: 40),
                Expanded(
                  child: Center(
                    child: Container(
                      padding: EdgeInsets.all(40),
                      decoration: BoxDecoration(
                        color: Color(0xFF44475a),
                        borderRadius: BorderRadius.circular(30),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.3),
                            blurRadius: 30,
                            offset: Offset(0, 15),
                          ),
                        ],
                      ),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            padding: EdgeInsets.all(30),
                            decoration: BoxDecoration(
                              color: Color(0xFFbd93f9).withOpacity(0.2),
                              shape: BoxShape.circle,
                            ),
                            child: Icon(
                              Icons.fitness_center,
                              color: Color(0xFFbd93f9),
                              size: 80,
                            ),
                          ),
                          SizedBox(height: 30),
                          Text(
                            'Hoş Geldiniz!',
                            style: TextStyle(
                              fontSize: 28,
                              fontWeight: FontWeight.w900,
                              color: Color(0xFFf8f8f2),
                            ),
                          ),
                          SizedBox(height: 16),
                          Text(
                            'AI teknolojisi ile egzersizlerinizi analiz edin ve doğru formda çalışın.',
                            style: TextStyle(
                              fontSize: 16,
                              color: Color(0xFF6272a4),
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
                SizedBox(height: 40),
                Container(
                  width: double.infinity,
                  height: 60,
                  child: ElevatedButton(
                    onPressed: () {
                      Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(builder: (_) => const HomeScreen()),
                      );
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0xFFbd93f9),
                      foregroundColor: Color(0xFFf8f8f2),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      elevation: 8,
                    ),
                    child: Text(
                      'Başla',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.w700),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
} 