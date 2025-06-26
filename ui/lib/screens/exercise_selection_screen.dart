import 'package:flutter/material.dart';
import 'camera_screen.dart';

class ExerciseSelectionScreen extends StatelessWidget {
  const ExerciseSelectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final exercises = [
      {'name': 'Biceps Curl', 'desc': 'Kol kaslarını geliştirir.'},
      {'name': 'Push-Up', 'desc': 'Göğüs ve kol kaslarını çalıştırır.'},
    ];
    return Scaffold(
      appBar: AppBar(
        title: const Text('Egzersiz Seçimi'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            mainAxisSpacing: 16,
            crossAxisSpacing: 16,
            childAspectRatio: 0.95,
          ),
          itemCount: exercises.length,
          itemBuilder: (context, index) {
            final ex = exercises[index];
            return _ExerciseCard(
              name: ex['name']!,
              desc: ex['desc']!,
              onStart: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const CameraScreen()),
                );
              },
            );
          },
        ),
      ),
    );
  }
}

class _ExerciseCard extends StatelessWidget {
  final String name;
  final String desc;
  final VoidCallback onStart;
  const _ExerciseCard({required this.name, required this.desc, required this.onStart});

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(name, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(desc, style: Theme.of(context).textTheme.bodyMedium),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: onStart,
                child: const Text('Başla'),
              ),
            ),
          ],
        ),
      ),
    );
  }
} 