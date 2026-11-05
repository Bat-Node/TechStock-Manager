-- TechStock Manager - banco de dados (SQL Server)
-- Selecione tudo no SSMS e clique em Executar (F5)

CREATE DATABASE TechStock;
GO

USE TechStock;
GO

-- Tabela de categorias
CREATE TABLE Categorias (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(80) NOT NULL UNIQUE
);

-- Tabela de fornecedores
CREATE TABLE Fornecedores (
    id INT IDENTITY(1,1) PRIMARY KEY,
    razao_social VARCHAR(120) NOT NULL,
    cnpj CHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(120)
);

-- Tabela de produtos (hardware, software e perifericos)
CREATE TABLE Produtos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    sku VARCHAR(30) NOT NULL UNIQUE,
    nome VARCHAR(120) NOT NULL,
    fabricante VARCHAR(80) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('Hardware', 'Software', 'Periferico')),
    especificacao VARCHAR(200),
    licenciamento VARCHAR(20) CHECK (licenciamento IN ('Assinatura', 'Perpetua', 'OEM')),
    preco DECIMAL(10,2) NOT NULL CHECK (preco > 0),
    estoque INT NOT NULL CHECK (estoque >= 0),
    estoque_minimo INT NOT NULL CHECK (estoque_minimo >= 0),
    localizacao VARCHAR(80),
    categoria_id INT NOT NULL FOREIGN KEY REFERENCES Categorias(id),
    fornecedor_id INT NOT NULL FOREIGN KEY REFERENCES Fornecedores(id)
);

-- Tabela de movimentacoes (entradas e saidas)
CREATE TABLE Movimentacoes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('Entrada', 'Saida')),
    quantidade INT NOT NULL CHECK (quantidade > 0),
    data_hora DATETIME NOT NULL DEFAULT GETDATE(),
    observacao VARCHAR(200),
    produto_id INT NOT NULL FOREIGN KEY REFERENCES Produtos(id)
);
GO

-- Dados de teste

INSERT INTO Categorias (nome) VALUES ('Armazenamento');
INSERT INTO Categorias (nome) VALUES ('Processamento');
INSERT INTO Categorias (nome) VALUES ('Suites de Escritorio');
INSERT INTO Categorias (nome) VALUES ('Sistemas Operacionais');

INSERT INTO Fornecedores (razao_social, cnpj, telefone, email)
VALUES ('Distribuidora Tech Brasil LTDA', '11222333000181', '(62) 3200-1000', 'vendas@techbrasil.com.br');
INSERT INTO Fornecedores (razao_social, cnpj, telefone, email)
VALUES ('Soft Licencas Corporativas SA', '22333444000172', '(11) 4000-2000', 'comercial@softlicencas.com.br');
INSERT INTO Fornecedores (razao_social, cnpj, telefone, email)
VALUES ('Hardware Center Atacado LTDA', '33444555000163', '(62) 3300-3000', 'contato@hwcenter.com.br');

INSERT INTO Produtos (sku, nome, fabricante, tipo, especificacao, licenciamento, preco, estoque, estoque_minimo, localizacao, categoria_id, fornecedor_id)
VALUES ('SSD-NVME-1TB', 'SSD NVMe 1TB', 'Kingston', 'Hardware', 'M.2 NVMe 1TB', NULL, 420.00, 15, 5, 'Prateleira A1', 1, 3);

INSERT INTO Produtos (sku, nome, fabricante, tipo, especificacao, licenciamento, preco, estoque, estoque_minimo, localizacao, categoria_id, fornecedor_id)
VALUES ('CPU-I5-12400', 'Processador Core i5-12400', 'Intel', 'Hardware', '6 nucleos, LGA1700', NULL, 1050.00, 4, 5, 'Prateleira B2', 2, 1);

INSERT INTO Produtos (sku, nome, fabricante, tipo, especificacao, licenciamento, preco, estoque, estoque_minimo, localizacao, categoria_id, fornecedor_id)
VALUES ('RAM-DDR4-16GB', 'Memoria RAM DDR4 16GB', 'Corsair', 'Hardware', 'DDR4 3200MHz', NULL, 260.00, 20, 8, 'Prateleira B1', 2, 3);

INSERT INTO Produtos (sku, nome, fabricante, tipo, especificacao, licenciamento, preco, estoque, estoque_minimo, localizacao, categoria_id, fornecedor_id)
VALUES ('M365-BUS-STD', 'Microsoft 365 Business Standard', 'Microsoft', 'Software', 'Assinatura anual, 1 usuario', 'Assinatura', 780.00, 30, 10, 'Cofre Digital', 3, 2);

INSERT INTO Produtos (sku, nome, fabricante, tipo, especificacao, licenciamento, preco, estoque, estoque_minimo, localizacao, categoria_id, fornecedor_id)
VALUES ('WIN11-PRO-ESD', 'Windows 11 Pro', 'Microsoft', 'Software', 'Licenca digital ESD', 'Perpetua', 890.00, 3, 5, 'Cofre Digital', 4, 2);

INSERT INTO Produtos (sku, nome, fabricante, tipo, especificacao, licenciamento, preco, estoque, estoque_minimo, localizacao, categoria_id, fornecedor_id)
VALUES ('OFF-2021-OEM', 'Office Home and Business 2021', 'Microsoft', 'Software', 'Licenca para 1 PC', 'OEM', 1100.00, 12, 4, 'Cofre Digital', 3, 2);
GO
