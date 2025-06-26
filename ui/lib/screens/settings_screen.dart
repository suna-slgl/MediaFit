import 'package:flutter/material.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool soundOn = true;
  bool darkMode = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ayarlar'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SwitchListTile(
              title: const Text('Sesli Bildirim'),
              value: soundOn,
              onChanged: (val) {
                setState(() => soundOn = val);
              },
              secondary: const Icon(Icons.volume_up),
            ),
            SwitchListTile(
              title: const Text('Karanlık Mod'),
              value: darkMode,
              onChanged: (val) {
                setState(() => darkMode = val);
                // Tema değişimi için provider veya benzeri bir yapı kullanılabilir
              },
              secondary: const Icon(Icons.dark_mode),
            ),
            const SizedBox(height: 32),
            const Text('Profil Bilgileri', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            ListTile(
              leading: const CircleAvatar(child: Icon(Icons.person)),
              title: const Text('Kullanıcı Adı'),
              subtitle: const Text('user@email.com'),
              trailing: IconButton(
                icon: const Icon(Icons.edit),
                onPressed: () {},
              ),
            ),
          ],
        ),
      ),
    );
  }
} 