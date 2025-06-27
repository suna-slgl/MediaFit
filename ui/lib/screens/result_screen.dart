import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class ResultScreen extends StatelessWidget {
  final Map<String, dynamic> rapor;
  const ResultScreen({super.key, required this.rapor});

  @override
  Widget build(BuildContext context) {
    // Veri analizi ve hesaplama
    double accuracy = 0.0;
    int correctCount = 0;
    int incorrectCount = 0;
    if (rapor.containsKey('accuracy')) {
      accuracy = (rapor['accuracy'] ?? 0.0).toDouble();
      correctCount = rapor['correct_count'] ?? 0;
      incorrectCount = rapor['incorrect_count'] ?? 0;
    } else if (rapor.containsKey('dogruluk')) {
      accuracy = (rapor['dogruluk'] ?? 0.0).toDouble();
      final acilar = rapor['acilar'] ?? [];
      correctCount = acilar.where((e) => e['correct'] == true).length;
      incorrectCount = acilar.where((e) => e['correct'] == false).length;
      if (accuracy == 0.0 && (correctCount + incorrectCount) > 0) {
        accuracy = correctCount / (correctCount + incorrectCount);
      }
    }
    int totalCount = correctCount + incorrectCount;
    // Eğer hiç veri yoksa, doğruluk 0% olmalı, %100 değil!
    if (totalCount == 0) {
      correctCount = 0;
      incorrectCount = 0;
      accuracy = 0.0;  // Hiç veri yoksa %0 doğruluk
    }
    if (accuracy > 1.0) accuracy = accuracy / 100.0;
    if (accuracy < 0.0) accuracy = 0.0;
    if (accuracy > 1.0) accuracy = 1.0;

    return Scaffold(
      backgroundColor: const Color(0xFF282a36),
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 32),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Büyük yüzde göstergesi
                Container(
                  width: 200,
                  height: 200,
                  decoration: BoxDecoration(
                    color: const Color(0xFF44475a),
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.3),
                        blurRadius: 30,
                        offset: const Offset(0, 10),
                      ),
                    ],
                  ),
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      TweenAnimationBuilder<double>(
                        tween: Tween<double>(begin: 0, end: accuracy),
                        duration: Duration(milliseconds: 800),
                        builder: (context, value, child) {
                          return CircularProgressIndicator(
                            value: value,
                            strokeWidth: 18,
                            backgroundColor: Colors.transparent,
                            valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF44475a)),
                          );
                        },
                      ),
                      Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            '${(accuracy * 100).toStringAsFixed(1)}%',
                            style: const TextStyle(
                              fontSize: 48,
                              fontWeight: FontWeight.w900,
                              color: Color(0xFFf8f8f2),
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Doğruluk',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFF6272a4),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 40),
                // Modern Dracula pasta grafik
                Container(
                  width: double.infinity,
                  constraints: const BoxConstraints(maxWidth: 340),
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
                  decoration: BoxDecoration(
                    color: const Color(0xFF44475a),
                    borderRadius: BorderRadius.circular(28),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.25),
                        blurRadius: 20,
                        offset: const Offset(0, 8),
                      ),
                    ],
                  ),
                  child: Column(
                    children: [
                      const Text(
                        'Doğru/Yanlış Dağılımı',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFFf8f8f2),
                        ),
                      ),
                      const SizedBox(height: 8),
                      SizedBox(
                        height: 120,
                        child: PieChart(
                          PieChartData(
                            sections: [
                              if (correctCount > 0)
                                PieChartSectionData(
                                  value: correctCount.toDouble(),
                                  title: '',
                                  color: const Color(0xFF50fa7b),
                                  radius: 38,
                                ),
                              if (incorrectCount > 0)
                                PieChartSectionData(
                                  value: incorrectCount.toDouble(),
                                  title: '',
                                  color: const Color(0xFFff5555),
                                  radius: 38,
                                ),
                            ],
                            centerSpaceRadius: 32,
                            sectionsSpace: 2,
                            startDegreeOffset: -90,
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),
                      Wrap(
                        alignment: WrapAlignment.center,
                        spacing: 24,
                        children: [
                          _LegendItem(
                            color: const Color(0xFF50fa7b),
                            label: 'Doğru',
                            value: correctCount.toString(),
                          ),
                          _LegendItem(
                            color: const Color(0xFFff5555),
                            label: 'Yanlış',
                            value: incorrectCount.toString(),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 40),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    icon: Icon(Icons.home, color: Color(0xFFf8f8f2)),
                    label: Text(
                      'Anasayfaya Dön',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFFf8f8f2),
                      ),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0xFFbd93f9),
                      padding: EdgeInsets.symmetric(vertical: 18),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
                      elevation: 8,
                    ),
                    onPressed: () {
                      Navigator.of(context).popUntil((route) => route.isFirst);
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

class _LegendItem extends StatelessWidget {
  final Color color;
  final String label;
  final String value;

  const _LegendItem({
    required this.color,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 16,
          height: 16,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
          ),
        ),
        const SizedBox(width: 8),
        Text(
          label,
          style: const TextStyle(
            fontSize: 15,
            fontWeight: FontWeight.w600,
            color: Color(0xFFf8f8f2),
          ),
        ),
        const SizedBox(width: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 13,
            color: Color(0xFF6272a4),
          ),
        ),
      ],
    );
  }
} 