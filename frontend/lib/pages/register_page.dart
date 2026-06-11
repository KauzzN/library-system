import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final usernameController = TextEditingController();

  final emailController = TextEditingController();

  final passwordController = TextEditingController();

  bool loading = false;

  Future<void> register() async {
    setState(() {
      loading = true;
    });

    try {
      final response = await http.post(
        Uri.parse("http://127.0.0.1:5000/manager/create"),

        headers: {"Content-Type": "application/json"},

        body: jsonEncode({
          "login": usernameController.text,
          "email": emailController.text,
          "senha": passwordController.text,
        }),
      );

      print("Status: ${response.statusCode}");

      print("Body: ${response.body}");

      final data = jsonDecode(response.body);

      if (response.statusCode == 201) {
        if (!mounted) return;

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Conta criada com sucesso")),
        );

        Navigator.pop(context);
      } else {
        if (!mounted) return;

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(data["error"] ?? "Erro ao criar conta")),
        );
      }
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Erro: $e")));
    }

    setState(() {
      loading = false;
    });
  }

  @override
  void dispose() {
    usernameController.dispose();
    emailController.dispose();
    passwordController.dispose();

    super.dispose();
  }

  Widget buildField({
    required TextEditingController controller,
    required String label,
    required IconData icon,
    bool obscure = false,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),

      child: TextField(
        controller: controller,
        obscureText: obscure,

        decoration: InputDecoration(
          labelText: label,

          prefixIcon: Icon(icon),

          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Criar Conta")),

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),

        child: Column(
          children: [
            const SizedBox(height: 20),

            const Icon(Icons.person_add, size: 80, color: Colors.indigo),

            const SizedBox(height: 20),

            buildField(
              controller: usernameController,
              label: "Nome",
              icon: Icons.person,
            ),

            buildField(
              controller: emailController,
              label: "Email",
              icon: Icons.email,
            ),

            buildField(
              controller: passwordController,
              label: "Senha",
              icon: Icons.lock,
              obscure: true,
            ),

            const SizedBox(height: 20),

            SizedBox(
              width: double.infinity,
              height: 50,

              child: ElevatedButton.icon(
                onPressed: loading ? null : register,

                icon: const Icon(Icons.check),

                label: loading
                    ? const CircularProgressIndicator()
                    : const Text("Criar Conta"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
