import 'package:flutter/material.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';

class CameraScreen extends StatelessWidget {
  const CameraScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Canlı Analiz (Python Stream)'), centerTitle: true),
      body: Center(
        child: Mjpeg(
          stream: 'http://192.168.1.101:5000/video_feed', // Python sunucunuzun IP'sini ve portunu girin
          isLive: true,
          error: (context, error, stack) => const Text('Stream yüklenemedi'),
        ),
      ),
    );
  }
} 