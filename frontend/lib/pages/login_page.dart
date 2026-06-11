import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:library_system_mobile/pages/forgot_password_page.dart';
import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';
import 'package:library_system_mobile/pages/home_page.dart';
import 'package:library_system_mobile/pages/register_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  Future<void> login() async {
    final email = emailController.text.trim();
    final password = passwordController.text;

    try {
      final response = await http.post(
        Uri.parse("http://127.0.0.1:5000/auth/login"),

        headers: {"Content-Type": "application/json"},

        body: jsonEncode({"email": email, "senha": password}),
      );

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        final prefs = await SharedPreferences.getInstance();

        await prefs.setString("token", data["token"]);

        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(data["message"])));

        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const HomePage()),
        );

        // depois vamos navegar pra Home
      } else {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(data["error"])));
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Erro ao conectar com o servidor")),
      );

      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF3F4F6),

      body: Center(
        child: SingleChildScrollView(
          child: Container(
            width: 350,
            padding: const EdgeInsets.all(24),

            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(20),

              boxShadow: const [
                BoxShadow(blurRadius: 10, color: Colors.black12),
              ],
            ),

            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(
                  Icons.menu_book_rounded,
                  size: 80,
                  color: Colors.indigo,
                ),

                const SizedBox(height: 20),

                const Text(
                  "Bem-vindo",
                  style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                ),

                const SizedBox(height: 8),

                const Text(
                  "Sistema de Biblioteca Digital",
                  style: TextStyle(color: Colors.grey),
                ),

                const SizedBox(height: 30),

                TextField(
                  controller: emailController,

                  decoration: InputDecoration(
                    labelText: "Email",
                    prefixIcon: const Icon(Icons.email),

                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),

                const SizedBox(height: 16),

                TextField(
                  controller: passwordController,
                  obscureText: true,

                  decoration: InputDecoration(
                    labelText: "Senha",
                    prefixIcon: const Icon(Icons.lock),

                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),

                const SizedBox(height: 24),

                SizedBox(
                  width: double.infinity,
                  height: 50,

                  child: ElevatedButton(
                    onPressed: login,

                    child: const Text("Entrar"),
                  ),
                ),

                const SizedBox(height: 16),

                TextButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const ForgotPasswordPage(),
                      ),
                    );
                  },

                  child: const Text("Esqueci minha senha"),
                ),

                TextButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const RegisterPage()),
                    );
                  },
                  child: const Text("Criar conta"),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
