import 'package:flutter/material.dart';

class ReportsScreen extends StatelessWidget {
  const ReportsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Raporlarım'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Haftalık İstatistikler', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            Container(
              height: 180,
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.blueGrey.withOpacity(0.08),
                borderRadius: BorderRadius.circular(16),
              ),
              child: const Center(child: Text('LineChart/BarChart (Grafik Placeholder)')),
            ),
            const SizedBox(height: 32),
            const Text('Önceki Egzersizler', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            Expanded(
              child: ListView(
                children: const [
                  ListTile(
                    leading: Icon(Icons.fitness_center),
                    title: Text('Push-Up'),
                    subtitle: Text('Başarı: %85'),
                    trailing: Text('2 gün önce'),
                  ),
                  ListTile(
                    leading: Icon(Icons.fitness_center),
                    title: Text('Squat'),
                    subtitle: Text('Başarı: %78'),
                    trailing: Text('4 gün önce'),
                  ),
                  ListTile(
                    leading: Icon(Icons.fitness_center),
                    title: Text('Plank'),
                    subtitle: Text('Başarı: %92'),
                    trailing: Text('1 hafta önce'),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
} 