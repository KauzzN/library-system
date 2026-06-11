import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class CreateBookPage extends StatefulWidget {
  const CreateBookPage({super.key});

  @override
  State<CreateBookPage> createState() => _CreateBookPageState();
}

class _CreateBookPageState extends State<CreateBookPage> {
  final nomeController = TextEditingController();
  final categoriaController = TextEditingController();
  final statusController = TextEditingController();
  final estoqueController = TextEditingController();

  bool loading = false;
  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();

    return prefs.getString("token");
  }

  Future<void> createBook() async {
    setState(() {
      loading = true;
    });

    try {
      final token = await getToken();

      final response = await http.post(
        Uri.parse("http://127.0.0.1:5000/books/create"),

        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token",
        },

        body: jsonEncode({
          "nome": nomeController.text,
          "categoria": categoriaController.text,
          "status": statusController.text,
          "estoque": int.parse(estoqueController.text),
        }),
      );

      print("http://127.0.0.1:5000/books/create");
      print("Status: ${response.statusCode}");
      print("Body: ${response.body}");

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        if (!mounted) return;

        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(data["message"])));

        nomeController.clear();
        categoriaController.clear();
        statusController.clear();
        estoqueController.clear();
      } else {
        if (!mounted) return;

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(data["mensagem"] ?? "Erro ao cadastrar livro"),
          ),
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
    nomeController.dispose();
    categoriaController.dispose();
    statusController.dispose();
    estoqueController.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Cadastrar Livro"), centerTitle: true),

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),

        child: Column(
          children: [
            TextField(
              controller: nomeController,

              decoration: const InputDecoration(
                labelText: "Nome do Livro",
                prefixIcon: Icon(Icons.menu_book),
                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 16),

            TextField(
              controller: categoriaController,

              decoration: const InputDecoration(
                labelText: "Categoria",
                prefixIcon: Icon(Icons.category),
                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 16),

            TextField(
              controller: statusController,

              decoration: const InputDecoration(
                labelText: "Status",
                prefixIcon: Icon(Icons.info),
                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 16),

            TextField(
              controller: estoqueController,
              keyboardType: TextInputType.number,

              decoration: const InputDecoration(
                labelText: "Estoque",
                prefixIcon: Icon(Icons.inventory),
                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 24),

            SizedBox(
              width: double.infinity,
              height: 50,

              child: ElevatedButton.icon(
                onPressed: loading ? null : createBook,

                icon: const Icon(Icons.save),

                label: loading
                    ? const CircularProgressIndicator()
                    : const Text("Cadastrar Livro"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
