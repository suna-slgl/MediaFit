import 'package:flutter/material.dart';

class ReportsScreen extends StatelessWidget {
  const ReportsScreen({super.key});

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
                    Text('Raporlar', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, color: Color(0xFFf8f8f2))),
                    CircleAvatar(
                      radius: 25,
                      backgroundColor: Color(0xFF44475a),
                      child: Icon(Icons.person, color: Color(0xFFf8f8f2), size: 30),
                    ),
                  ],
                ),
                SizedBox(height: 8),
                Text('Egzersiz geçmişiniz:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: Color(0xFF6272a4))),
                SizedBox(height: 20),
                Expanded(
                  child: ListView.builder(
                    itemCount: 5,
                    itemBuilder: (context, index) {
                      return _ReportCard(
                        title: 'Egzersiz ${index + 1}',
                        date: '${DateTime.now().day - index}.${DateTime.now().month}.${DateTime.now().year}',
                        accuracy: 85 - (index * 5),
                        onTap: () {},
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

class _ReportCard extends StatelessWidget {
  final String title;
  final String date;
  final int accuracy;
  final VoidCallback onTap;

  const _ReportCard({
    required this.title,
    required this.date,
    required this.accuracy,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: EdgeInsets.only(bottom: 16),
        padding: EdgeInsets.all(20),
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
        ),
        child: Row(
          children: [
            Container(
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Color(0xFFbd93f9).withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: Icon(Icons.bar_chart, color: Color(0xFFbd93f9), size: 30),
            ),
            SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w700,
                      color: Color(0xFFf8f8f2),
                    ),
                  ),
                  SizedBox(height: 4),
                  Text(
                    date,
                    style: TextStyle(
                      fontSize: 14,
                      color: Color(0xFF6272a4),
                    ),
                  ),
                ],
              ),
            ),
            Container(
              padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: accuracy >= 80 ? Color(0xFF50fa7b).withOpacity(0.2) : Color(0xFFffb86c).withOpacity(0.2),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                '$accuracy%',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w700,
                  color: accuracy >= 80 ? Color(0xFF50fa7b) : Color(0xFFffb86c),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
} 