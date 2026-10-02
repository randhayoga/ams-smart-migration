-- ========================================================
-- Master Categories Data Migration Script for MS SQL Server
-- Generated: 2026-09-30 09:30:58
-- Target Table: categories
-- ========================================================
SET IDENTITY_INSERT [categories] ON;
GO

INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (1, 'FUR', N'Furniture', '2018-04-05 19:22:48', '2018-04-05 19:22:48');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (2, 'ACC', N'Aksesoris', '2016-12-08 14:32:30', '2016-12-08 14:32:30');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (3, 'COMP', N'Computer', '2016-12-16 10:11:55', '2016-12-16 10:11:55');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (4, 'MON', N'Monitor', '2016-12-16 10:12:31', '2016-12-16 10:12:31');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (5, 'PERP', N'Peripheral', '2016-12-16 10:13:22', '2016-12-16 10:13:22');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (6, 'PRNT', N'Printer', '2016-12-16 10:14:53', '2016-12-16 10:14:53');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (7, 'SOFT', N'Software', '2016-12-16 10:15:22', '2016-12-16 10:15:22');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (8, 'PROP', N'Properti & Gedung', '2022-07-01 13:28:04', '2022-07-01 13:28:04');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (9, 'MES', N'Mesin', '2017-01-05 17:29:43', '2017-01-05 17:29:43');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (10, 'KEND', N'Kendaraan', '2023-06-13 14:02:32', '2023-06-13 14:02:32');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (11, 'ELEK', N'Elektronik', '2023-06-13 14:01:35', '2023-06-13 14:01:35');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (12, 'PDGR', N'Pendingin Ruangan', '2025-02-05 13:38:52', '2025-02-05 13:38:52');
INSERT INTO [categories] ([id], [code], [name], [created_at], [updated_at]) VALUES (13, 'TLKM', N'Telekomunikasi', '2025-02-06 10:47:01.000', '2025-02-06 10:47:01.000');

GO
SET IDENTITY_INSERT [categories] OFF;
GO