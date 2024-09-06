我们将把这个租借程序转换为WPF（Windows Presentation Foundation）应用程序。WPF是一个用于构建Windows桌面应用程序的UI框架，它可以提供更好的用户体验和界面。

### 计划

1. **UI设计**：使用XAML创建一个简单的界面来处理借用、归还和库存查询操作。
2. **数据库设计**：使用SQLite创建一个包含租借记录的数据库表。
3. **借用功能**：记录物品名称、借用人姓名和当前时间作为借用时间。
4. **归还功能**：更新数据库记录，标记物品已归还。
5. **库存查询功能**：查询当前所有未归还的物品。

### 实现步骤

#### 1. 创建WPF项目

1. 打开Visual Studio，创建一个新的 **WPF App (.NET Framework)** 项目。
2. 命名项目为 `RentalSystemWPF`。

#### 2. 安装SQLite支持

在NuGet包管理器中安装 `System.Data.SQLite`：

```sh
Install-Package System.Data.SQLite
```

#### 3. 设计WPF界面

在 `MainWindow.xaml` 文件中，使用以下XAML代码设计用户界面：

```xml
<Window x:Class="RentalSystemWPF.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Rental System" Height="350" Width="525">
    <Grid>
        <StackPanel Margin="10">
            <!-- 借用物品 -->
            <GroupBox Header="Borrow Item" Margin="0,0,0,10">
                <StackPanel>
                    <TextBox x:Name="ItemNameTextBox" PlaceholderText="Item Name" Margin="0,5"/>
                    <TextBox x:Name="BorrowerNameTextBox" PlaceholderText="Borrower Name" Margin="0,5"/>
                    <Button Content="Borrow" Click="BorrowButton_Click" Margin="0,5"/>
                </StackPanel>
            </GroupBox>
            
            <!-- 归还物品 -->
            <GroupBox Header="Return Item" Margin="0,0,0,10">
                <StackPanel>
                    <TextBox x:Name="ReturnItemNameTextBox" PlaceholderText="Item Name" Margin="0,5"/>
                    <TextBox x:Name="ReturnBorrowerNameTextBox" PlaceholderText="Borrower Name" Margin="0,5"/>
                    <Button Content="Return" Click="ReturnButton_Click" Margin="0,5"/>
                </StackPanel>
            </GroupBox>
            
            <!-- 查询库存 -->
            <Button Content="Check Inventory" Click="CheckInventoryButton_Click" Margin="0,0,0,10"/>
            <TextBox x:Name="InventoryTextBox" IsReadOnly="True" Height="100" TextWrapping="Wrap" VerticalScrollBarVisibility="Auto"/>
        </StackPanel>
    </Grid>
</Window>
```

#### 4. 实现代码逻辑

在 `MainWindow.xaml.cs` 文件中，编写以下C#代码以处理按钮点击事件，并与SQLite数据库进行交互：

```csharp
using System;
using System.Data.SQLite;
using System.Windows;

namespace RentalSystemWPF
{
    public partial class MainWindow : Window
    {
        private SQLiteConnection sqlite_conn;
        private SQLiteCommand sqlite_cmd;

        public MainWindow()
        {
            InitializeComponent();
            InitializeDatabase();
        }

        private void InitializeDatabase()
        {
            // 初始化SQLite数据库连接
            sqlite_conn = new SQLiteConnection("Data Source=rental_system.db;Version=3;");
            sqlite_conn.Open();

            // 创建租借记录表
            sqlite_cmd = sqlite_conn.CreateCommand();
            sqlite_cmd.CommandText = @"CREATE TABLE IF NOT EXISTS borrow_records (
                                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ItemName TEXT NOT NULL,
                                        BorrowerName TEXT NOT NULL,
                                        BorrowDate TEXT NOT NULL,
                                        ReturnDate TEXT)";
            sqlite_cmd.ExecuteNonQuery();
        }

        private void BorrowButton_Click(object sender, RoutedEventArgs e)
        {
            string itemName = ItemNameTextBox.Text;
            string borrowerName = BorrowerNameTextBox.Text;
            if (string.IsNullOrEmpty(itemName) || string.IsNullOrEmpty(borrowerName))
            {
                MessageBox.Show("Please enter both item name and borrower name.");
                return;
            }

            string borrowDate = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            sqlite_cmd = sqlite_conn.CreateCommand();
            sqlite_cmd.CommandText = @"INSERT INTO borrow_records (ItemName, BorrowerName, BorrowDate) 
                                       VALUES (@itemName, @borrowerName, @borrowDate)";
            sqlite_cmd.Parameters.AddWithValue("@itemName", itemName);
            sqlite_cmd.Parameters.AddWithValue("@borrowerName", borrowerName);
            sqlite_cmd.Parameters.AddWithValue("@borrowDate", borrowDate);
            sqlite_cmd.ExecuteNonQuery();

            MessageBox.Show($"'{itemName}' has been borrowed by {borrowerName} on {borrowDate}.");
        }

        private void ReturnButton_Click(object sender, RoutedEventArgs e)
        {
            string itemName = ReturnItemNameTextBox.Text;
            string borrowerName = ReturnBorrowerNameTextBox.Text;
            if (string.IsNullOrEmpty(itemName) || string.IsNullOrEmpty(borrowerName))
            {
                MessageBox.Show("Please enter both item name and borrower name.");
                return;
            }

            string returnDate = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            sqlite_cmd = sqlite_conn.CreateCommand();
            sqlite_cmd.CommandText = @"UPDATE borrow_records 
                                       SET ReturnDate = @returnDate 
                                       WHERE ItemName = @itemName AND BorrowerName = @borrowerName AND ReturnDate IS NULL";
            sqlite_cmd.Parameters.AddWithValue("@returnDate", returnDate);
            sqlite_cmd.Parameters.AddWithValue("@itemName", itemName);
            sqlite_cmd.Parameters.AddWithValue("@borrowerName", borrowerName);
            int rowsAffected = sqlite_cmd.ExecuteNonQuery();

            if (rowsAffected > 0)
            {
                MessageBox.Show($"'{itemName}' has been returned by {borrowerName} on {returnDate}.");
            }
            else
            {
                MessageBox.Show($"No matching record found for '{itemName}' borrowed by {borrowerName}.");
            }
        }

        private void CheckInventoryButton_Click(object sender, RoutedEventArgs e)
        {
            sqlite_cmd = sqlite_conn.CreateCommand();
            sqlite_cmd.CommandText = @"SELECT ItemName, BorrowerName, BorrowDate FROM borrow_records WHERE ReturnDate IS NULL";
            SQLiteDataReader reader = sqlite_cmd.ExecuteReader();

            InventoryTextBox.Clear();
            if (reader.HasRows)
            {
                InventoryTextBox.AppendText("Current borrowed items:\n");
                while (reader.Read())
                {
                    InventoryTextBox.AppendText($"Item: {reader["ItemName"]}, Borrower: {reader["BorrowerName"]}, Borrow Date: {reader["BorrowDate"]}\n");
                }
            }
            else
            {
                InventoryTextBox.AppendText("All items are returned.");
            }
            reader.Close();
        }
    }
}
```

### 运行步骤

1. 打开Visual Studio，创建一个新的WPF App项目。
2. 将上述XAML代码粘贴到 `MainWindow.xaml` 文件中，替换其现有内容。
3. 将C#代码粘贴到 `MainWindow.xaml.cs` 文件中，替换其现有内容。
4. 确保安装了 `System.Data.SQLite` 包。
5. 运行项目，使用界面进行借用、归还和库存查询操作。

### 后续步骤

- **W:** 是的，继续 - 添加更多功能或优化UI界面。
- **A:** 替代方法 - 使用其他UI框架或数据库。
- **S:** 解释 - 逐行解释代码工作原理。
- **D:** 迭代改进 - 提出三点改进或优化建议。
