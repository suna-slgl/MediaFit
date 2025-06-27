import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

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
                    Text('Ayarlar', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, color: Color(0xFFf8f8f2))),
                    CircleAvatar(
                      radius: 25,
                      backgroundColor: Color(0xFF44475a),
                      child: Icon(Icons.person, color: Color(0xFFf8f8f2), size: 30),
                    ),
                  ],
                ),
                SizedBox(height: 20),
                Expanded(
                  child: ListView(
                    children: [
                      _SettingsCard(
                        icon: Icons.notifications,
                        title: 'Bildirimler',
                        subtitle: 'Egzersiz hatırlatıcıları',
                        onTap: () {},
                      ),
                      _SettingsCard(
                        icon: Icons.language,
                        title: 'Dil',
                        subtitle: 'Türkçe',
                        onTap: () {},
                      ),
                      _SettingsCard(
                        icon: Icons.palette,
                        title: 'Tema',
                        subtitle: 'Dracula tema',
                        onTap: () {},
                      ),
                      _SettingsCard(
                        icon: Icons.help,
                        title: 'Yardım',
                        subtitle: 'Kullanım kılavuzu',
                        onTap: () {},
                      ),
                      _SettingsCard(
                        icon: Icons.info,
                        title: 'Hakkında',
                        subtitle: 'Uygulama bilgileri',
                        onTap: () {},
                      ),
                    ],
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

class _SettingsCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _SettingsCard({
    required this.icon,
    required this.title,
    required this.subtitle,
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
                color: Color(0xFFffb86c).withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: Color(0xFFffb86c), size: 30),
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
                    subtitle,
                    style: TextStyle(
                      fontSize: 14,
                      color: Color(0xFF6272a4),
                    ),
                  ),
                ],
              ),
            ),
            Icon(Icons.arrow_forward_ios, color: Color(0xFF6272a4), size: 20),
          ],
        ),
      ),
    );
  }
} 