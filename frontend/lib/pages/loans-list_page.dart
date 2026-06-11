import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class LoansPage extends StatefulWidget {
  const LoansPage({super.key});

  @override
  State<LoansPage> createState() => _LoansPageState();
}

class _LoansPageState extends State<LoansPage> {
  List loans = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    loadLoans();
  }

  Future<void> deleteLoan(String cpf) async {
    final response = await http.post(
      Uri.parse("http://127.0.0.1:5000/returns/delete"),

      headers: {"Content-Type": "application/json"},

      body: jsonEncode({"cpf": cpf}),
    );

    print(response.statusCode);
    print(response.body);

    if (response.statusCode == 200) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Empréstimo removido com sucesso")),
      );

      loadLoans();
    } else {
      final data = jsonDecode(response.body);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(data["error"] ?? "Erro ao remover empréstimo")),
      );
    }
  }

  Future<void> loadLoans() async {
    try {
      final prefs = await SharedPreferences.getInstance();

      final token = prefs.getString("token");

      final response = await http.get(
        Uri.parse("http://127.0.0.1:5000/loans/read"),
        headers: {
          "Authorization": "Bearer $token",
          "Content-Type": "application/json",
        },
      );

      print("Status: ${response.statusCode}");
      print("Body: ${response.body}");

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        setState(() {
          loans = data;
          loading = false;
        });
      } else {
        setState(() {
          loading = false;
        });

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(data["error"] ?? "Erro ao carregar empréstimos"),
          ),
        );
      }
    } catch (e) {
      print(e);

      setState(() {
        loading = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Erro ao conectar ao servidor")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Empréstimos")),

      body: loading
          ? const Center(child: CircularProgressIndicator())
          : loans.isEmpty
          ? const Center(child: Text("Nenhum empréstimo encontrado"))
          : ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: loans.length,

              itemBuilder: (context, index) {
                final loan = loans[index];

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),

                  child: ListTile(
                    leading: const Icon(Icons.person, color: Colors.indigo),

                    title: Text(loan["nome"]),

                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,

                      children: [
                        Text("CPF: ${loan["cpf"]}"),

                        Text("Telefone: ${loan["telefone"]}"),

                        Text("Prazo: ${loan["qtd_dias"]} dias"),

                        Text("Livro: ${loan["livro"]}"),
                      ],
                    ),

                    trailing: IconButton(
                      icon: const Icon(Icons.delete, color: Colors.red),

                      onPressed: () {
                        deleteLoan(loan["cpf"]);
                      },
                    ),
                  ),
                );
              },
            ),
    );
  }
}
