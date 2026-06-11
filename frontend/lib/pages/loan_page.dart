import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class LoanPage extends StatefulWidget {
  const LoanPage({super.key});

  @override
  State<LoanPage> createState() => _LoanPageState();
}

class _LoanPageState extends State<LoanPage> {
  final diasController = TextEditingController();
  final nomeController = TextEditingController();
  final telefoneController = TextEditingController();
  final cpfController = TextEditingController();

  bool loading = false;

  List books = [];
  int? selectedBookId;

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();

    return prefs.getString("token");
  }

  Future<void> loadBooks() async {
    try {
      final token = await getToken();

      final response = await http.get(
        Uri.parse("http://127.0.0.1:5000/books/list"),
        headers: {"Authorization": "Bearer $token"},
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        setState(() {
          books = data;
        });
      }
    } catch (e) {
      print(e);
    }
  }

  Future<void> createLoan() async {
    setState(() {
      loading = true;
    });

    try {
      if (selectedBookId == null) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text("Selecione um livro")));
        return;
      }

      setState(() {
        loading = true;
      });

      final token = await getToken();

      final response = await http.post(
        Uri.parse("http://127.0.0.1:5000/loans/create"),

        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token",
        },

        body: jsonEncode({
          "dias": int.parse(diasController.text),
          "nome": nomeController.text,
          "telefone": telefoneController.text,
          "cpf": cpfController.text,
          "idlivro": selectedBookId,
        }),
      );

      print("Status: ${response.statusCode}");
      print("Body: ${response.body}");

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        if (!mounted) return;

        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(data["mensagem"])));

        diasController.clear();
        nomeController.clear();
        telefoneController.clear();
        cpfController.clear();
        setState(() {
          selectedBookId = null;
        });
      } else {
        if (!mounted) return;

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(data["error"] ?? "Erro ao criar empréstimo")),
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
  void initState() {
    super.initState();
    loadBooks();
  }

  @override
  void dispose() {
    diasController.dispose();
    nomeController.dispose();
    telefoneController.dispose();
    cpfController.dispose();
    super.dispose();
  }

  Widget buildField({
    required TextEditingController controller,
    required String label,
    required IconData icon,
    TextInputType keyboardType = TextInputType.text,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: TextField(
        controller: controller,
        keyboardType: keyboardType,

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
      appBar: AppBar(title: const Text("Novo Empréstimo")),

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),

        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.only(bottom: 16),

              child: DropdownButtonFormField<int>(
                value: selectedBookId,

                decoration: InputDecoration(
                  labelText: "Livro",
                  prefixIcon: const Icon(Icons.menu_book),

                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),

                items: books.map<DropdownMenuItem<int>>((book) {
                  return DropdownMenuItem<int>(
                    value: book["id"],
                    child: Text(book["nome"]),
                  );
                }).toList(),

                onChanged: (value) {
                  setState(() {
                    selectedBookId = value;
                  });
                },
              ),
            ),
            buildField(
              controller: nomeController,
              label: "Nome do Cliente",
              icon: Icons.person,
            ),

            buildField(
              controller: telefoneController,
              label: "Telefone",
              icon: Icons.phone,
              keyboardType: TextInputType.phone,
            ),

            buildField(
              controller: cpfController,
              label: "CPF",
              icon: Icons.badge,
              keyboardType: TextInputType.number,
            ),

            buildField(
              controller: diasController,
              label: "Dias do Empréstimo",
              icon: Icons.calendar_today,
              keyboardType: TextInputType.number,
            ),

            const SizedBox(height: 20),

            SizedBox(
              width: double.infinity,
              height: 50,

              child: ElevatedButton.icon(
                onPressed: loading ? null : createLoan,

                icon: const Icon(Icons.assignment),

                label: loading
                    ? const CircularProgressIndicator()
                    : const Text("Registrar Empréstimo"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
