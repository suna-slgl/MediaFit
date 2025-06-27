import 'package:flutter/material.dart';
import 'camera_screen.dart';

class ExerciseSelectionScreen extends StatelessWidget {
  const ExerciseSelectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final exercises = [
      {'icon': Icons.fitness_center, 'label': 'Biceps Curl'},
      {'icon': Icons.push_pin, 'label': 'Push-Up'},
    ];
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
                    Text('Egzersiz Seçimi', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, color: Color(0xFFf8f8f2))),
                    CircleAvatar(
                      radius: 25,
                      backgroundColor: Color(0xFF44475a),
                      child: Icon(Icons.person, color: Color(0xFFf8f8f2), size: 30),
                    ),
                  ],
                ),
                SizedBox(height: 8),
                Text('Bir egzersiz seçin:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: Color(0xFF6272a4))),
                SizedBox(height: 20),
                Expanded(
                  child: GridView.builder(
                    itemCount: exercises.length,
                    gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2,
                      mainAxisSpacing: 16,
                      crossAxisSpacing: 16,
                      childAspectRatio: 0.85,
                    ),
                    itemBuilder: (context, i) {
                      final ex = exercises[i];
                      return _ExerciseCard(
                        icon: ex['icon'] as IconData,
                        label: ex['label'] as String,
                        selected: false,
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => const CameraScreen()),
                          );
                        },
                      );
                    },
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

class _ExerciseCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool selected;
  final VoidCallback onTap;
  const _ExerciseCard({required this.icon, required this.label, required this.selected, required this.onTap});
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: Color(0xFF44475a),
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.3),
              blurRadius: 20,
              offset: Offset(0, 10),
            ),
          ],
          border: selected ? Border.all(color: Color(0xFFbd93f9), width: 3) : null,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Color(0xFFbd93f9).withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: Color(0xFFbd93f9), size: 50),
            ),
            SizedBox(height: 16),
            Text(
              label,
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w700,
                color: Color(0xFFf8f8f2),
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
} 