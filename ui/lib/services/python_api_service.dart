import 'dart:convert';
import 'package:http/http.dart' as http;

class PythonApiService {
  static const String baseUrl = 'http://192.168.1.101:5000'; // Gerçek cihaz için yerel ağ IP adresi

  static Future<Map<String, dynamic>?> analyzeExercise(Map<String, dynamic> data) async {
    final url = Uri.parse('$baseUrl/analyze');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print('API Hatası: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('API Hatası: $e');
      return null;
    }
  }
} 