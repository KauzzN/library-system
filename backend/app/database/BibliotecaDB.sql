 -- Projeto BibliotecaDB
 -- Requisito: No mínimo 4 tabelas relacionadas entre si, ou seja, cada tabela deve ter algum relacionamento
 -- Dicentes: Austregíselo Junior, 
 
 
 -- Criando banco de dados e tabelas
CREATE DATABASE BibliotecaDB;
USE BibliotecaDB;

drop table `emprestimo`;
drop table `logger`;
drop table `gerente`;
drop table `livro`;


  create table `gerente` (
  `idgerente` int primary key auto_increment,
  `login`varchar(100) not null,
  `senha` varchar(15) not null,
  `email` varchar(100) not null unique);

  CREATE TABLE `livro` (
  `idlivro` int primary key auto_increment,
  `nome` varchar(100) not null,
  `autor` varchar(120) not null,
  `categoria` varchar(100) not null,
  `status` varchar(50) not null,
  `estoque` int not null,
  constraint `chk_livros_estoque` check (`estoque` >= 0),
  constraint `chk_livro_status` check (`status` in ('Disponível', 'Reservado')));
  
  create table `emprestimo` (
  `idemprestimo` int primary key auto_increment,
  `data_emprestimo` DATE NOT NULL DEFAULT (CURRENT_DATE),
  `qtd_dias` int not null,
  `nome`varchar(100) not null,
  `telefone` varchar(20) not null,
  `cpf` varchar(15) not null unique,
  `fk_idlivro` INT NOT NULL,
	CONSTRAINT `fk_emprestimo_livro` FOREIGN KEY (`fk_idlivro`) REFERENCES livro(`idlivro`),
	CONSTRAINT `chk_emprestimo_qtd_dias` CHECK (`qtd_dias` > 0 and `qtd_dias` <= 60));
    
    create table `logger`(
	`idlog` INT PRIMARY KEY AUTO_INCREMENT,
    `mensagem` VARCHAR(255),
    `data` DATETIME DEFAULT (CURRENT_TIMESTAMP));
  
									-- Fluxos do gerente --
-- Listar gerentes --
Delimiter %%
Create procedure GetGerente()
begin
	select g.login, g.senha, g.email 
	from gerente g;
end %%
Delimiter ;
drop procedure GetGerente;
Call GetGerente();

-- Adicionar gerente -- 
Delimiter %%
Create procedure InsertGerente(in p_login varchar(100), in p_senha varchar(15), in p_email varchar(100))
begin
	INSERT INTO gerente (login, senha, email)
	VALUES (p_login, p_senha, p_email);
end %%
Delimiter ;
drop procedure InsertGerente;
Call InsertGerente(@login, @senha, @email);

-- Atualizar gerente -- 
Delimiter %%
Create procedure AtualizarGerente(in p_login varchar(100), in p_senha varchar(15), in p_email varchar(100))
begin
	update gerente 
		set login = p_login, senha = p_senha, email = p_email
		where login = p_login;
end %%
Delimiter ;
drop procedure AtualizarGerente;
Call AtualizarGerente(@login, @senha, @email);
								-- Fluxo de Login --
-- Login --
Delimiter %%
Create procedure Login(in p_email varchar(100), in p_senha varchar(15))
begin
	select idgerente, email, senha
    from gerente 
		where email = p_email and senha = p_senha;
end %%
Delimiter ;
drop procedure Login;
Call Login(@email, @senha);

-- Atualizar senha -- 
Delimiter %%
Create procedure AtualizarSenha(in p_senha varchar(15), in p_email varchar(100))
begin
	update gerente 
		set senha = p_senha
		where email = p_email;
end %%
Delimiter ;
drop procedure AtualizarSenha;
Call AtualizarSenha(@senha, @email);

-- Recuperar senha -- 
Delimiter %%
Create procedure RecuperarSenha(in p_email varchar(100))
begin
	select idgerente, login, email
    from gerente 
		where email = p_email;
end %%
Delimiter ;
drop procedure RecuperarSenha;
Call RecuperarSenha(@email);

-- Delete Gerente -- 
Delimiter %%
Create procedure DeleteGerente(in p_idgerente varchar(100))
begin
	Delete from gerente
    where idgerente = p_idgerente;
end %%
Delimiter ;
drop procedure DeleteGerente;
Call DeleteGerente(@idgerente);



									-- Fluxos do livro --
-- Listar livros --
Delimiter %%
Create procedure GetLivros()
begin
	select * from livro;
end %%
Delimiter ;
drop procedure GetLivros;
Call GetLivros();

-- Add livros -- 
Delimiter %%
Create procedure InsertLivro(in p_nome varchar(100), in p_categoria varchar(100), in p_status varchar(50), in p_estoque int)
begin
	INSERT INTO livro (nome, categoria, status, estoque)
	VALUES (p_nome, p_categoria, p_status, p_estoque );
end %%
Delimiter ;
drop procedure InsertLivro;
Call InsertLivro(@nome, @categoria, @status, @estoque);

-- Atualizar livro --
Delimiter %%
Create procedure AtualizarLivro(in p_idlivro int, in p_nome varchar(100), in p_categoria varchar(100), in p_status varchar(50), in p_estoque int)
begin
	update livro 
		set nome = p_nome, categoria = p_categoria, status = p_status, estoque = p_estoque
		where idlivro = p_idlivro;
end %%
Delimiter ;
drop procedure AtualizarLivro;
Call AtualizarLivro(@idlivro ,@nome, @categoria, @status, @estoque);

-- Delete livros -- 
Delimiter %%
Create procedure DeleteLivro(in p_idlovro int)
begin
	Delete from livro
    where idlivro = p_idlovro;
end %%
Delimiter ;
drop procedure DeleteLivro;
Call DeleteLivro(@nome);



									-- Cliente --
-- Insert --
Delimiter %%
Create procedure InsertCliente(in p_nome varchar(100), in p_cpf varchar(15), in p_telefone varchar(20), in p_endereco varchar(100))
begin
	INSERT INTO cliente (nome, cpf, telefone, endereco)
	VALUES (p_nome, p_cpf, p_telefone, p_endereco);
end %%
Delimiter ;
drop procedure InsertCliente;
Call InsertCliente(@nome, @cpf, @telefone, @endereco);

-- get --
Delimiter %%
Create procedure GetClientes()
begin
	select * from cliente;
end %%
Delimiter ;
drop procedure GetClientes;
Call GetClientes();

									-- Emprestimo --
Delimiter %%
Create procedure InsertEmprestimo(in p_dias int, in p_nome varchar(100), in p_telefone varchar(20), in p_cpf varchar(15), in p_fkidLivro int)
begin
	INSERT INTO emprestimo (qtd_dias, nome, telefone, cpf, fk_idlivro)
	VALUES (p_dias, p_nome, p_telefone, p_cpf, p_fkidLivro);
end %%
Delimiter ;
drop procedure InsertEmprestimo;
Call InsertEmprestimo(@dias, @p_nome, @p_telefone, @p_cpf, @fk_idlivro);

DELIMITER $$
CREATE TRIGGER trg_validar_estoque
BEFORE INSERT ON emprestimo
FOR EACH ROW
BEGIN
    DECLARE v_estoque INT;

    SELECT estoque INTO v_estoque
    FROM livro
    WHERE idlivro = NEW.fk_idlivro;

    IF v_estoque <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT ='Nao existem exemplares disponiveis';
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_emprestimo_reserva
AFTER INSERT ON emprestimo
FOR EACH ROW
BEGIN
	 DECLARE v_estoque INT;
     
     UPDATE livro
		SET estoque = estoque - 1
		WHERE idlivro = NEW.fk_idlivro;
        
     SELECT estoque INTO v_estoque
        FROM livro
        WHERE idlivro = NEW.fk_idlivro;

     IF v_estoque <= 0 THEN
        UPDATE livro
		set status = 'Reservado'
        WHERE idlivro = NEW.fk_idlivro;
    END IF;
END $$
DELIMITER ;

drop trigger trg_emprestimo_reserva;

									-- Devolução --
Delimiter %%
Create procedure DeleteEmprestimo(in p_cpf varchar(100))
begin
	Delete from emprestimo
    where cpf = p_cpf;
end %%
Delimiter ;
drop procedure DeleteEmprestimo;
Call DeleteEmprestimo(@p_cpf);

    
DELIMITER $$
CREATE TRIGGER trg_devolucao
AFTER DELETE ON emprestimo
FOR EACH ROW
BEGIN
    UPDATE livro
    SET estoque = estoque + 1,
        status = 'Disponível'
    WHERE idlivro = OLD.fk_idlivro;
END $$
DELIMITER ;

								  -- logger --
DELIMITER $$
CREATE TRIGGER trg_log_emprestimo
AFTER INSERT ON emprestimo
FOR EACH ROW
BEGIN
	
    INSERT INTO logger(mensagem) VALUES
    (concat('Emprestimo realizado. Id inscrição: ', 
    NEW.idemprestimo));
END $$
DELIMITER ;

                                 -- Testando --
select * from emprestimo;
select * from livro;
select * from cliente;
select * from gerente;

update livro
set status = "Reservado"
where idlivro = 6;

DELETE FROM gerente;








