import json
import os
from datetime import datetime

# File untuk menyimpan data
DATA_FILE = "todo_data.json"

# Daftar kategori yang tersedia
CATEGORIES = {
    '1': 'Tugas Sekolah',
    '2': 'Pekerjaan Rumah',
    '3': 'Acara Keluarga',
    '4': 'Agenda Organisasi',
    '5': 'Ulang Tahun',
    '6': 'Pertemuan OSIS',
    '7': 'Jadwal Olahraga',
    '8': 'Hari Penting Lainnya',
    '9': 'Jadwal Mancing',
    '10': 'Nongkrong'
}

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_data()
    
    def load_data(self):
        """Memuat data dari file JSON"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                self.tasks = []
        else:
            self.tasks = []
    
    def save_data(self):
        """Menyimpan data ke file JSON"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def add_task(self, title, description="", category="Tugas Sekolah"):
        """Menambah tugas baru"""
        # Generate ID baru berdasarkan tugas terakhir
        new_id = max([t["id"] for t in self.tasks], default=0) + 1
        
        task = {
            "id": new_id,
            "title": title,
            "description": description,
            "category": category,
            "status": "Belum Selesai",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_data()
        print(f"\n✅ Tugas '{title}' berhasil ditambahkan!\n")
    
    def view_tasks(self):
        """Menampilkan semua tugas"""
        if not self.tasks:
            print("\n📋 Tidak ada tugas. Silakan tambahkan tugas terlebih dahulu!\n")
            return
        
        print("\n" + "═"*90)
        print("📋 DAFTAR TUGAS".center(90))
        print("═"*90)
        
        for task in self.tasks:
            status_icon = "✅" if task["status"] == "Selesai" else "⭕"
            print(f"\n[ID: {task['id']:02d}] {status_icon} {task['title']}")
            print(f"   │ Kategori    : {task['category']}")
            print(f"   │ Status      : {task['status']}")
            if task['description']:
                print(f"   │ Deskripsi   : {task['description']}")
            print(f"   └─ Dibuat      : {task['created_at']}")
        
        print("\n" + "═"*90 + "\n")
    
    def edit_task(self, task_id):
        """Mengedit tugas"""
        task = self.find_task(task_id)
        if not task:
            print(f"\n❌ Tugas dengan ID {task_id} tidak ditemukan!\n")
            return
        
        print(f"\n📝 Edit Tugas: {task['title']}")
        print("(Tekan Enter untuk skip/tidak mengubah)")
        print("-" * 50)
        
        new_title = input(f"Judul ({task['title']}): ").strip()
        if new_title:
            task['title'] = new_title
        
        new_description = input(f"Deskripsi ({task['description'] or 'Kosong'}): ").strip()
        if new_description:
            task['description'] = new_description
        
        print("\nKategori tersedia:")
        for key, cat in CATEGORIES.items():
            marker = "→" if CATEGORIES[key] == task['category'] else " "
            print(f"  {marker} {key:2}. {cat}")
        
        new_category_choice = input(f"\nKategori ({task['category']}): ").strip()
        if new_category_choice in CATEGORIES:
            task['category'] = CATEGORIES[new_category_choice]
        
        self.save_data()
        print(f"\n✅ Tugas berhasil diperbarui!\n")
    
    def delete_task(self, task_id):
        """Menghapus tugas"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                title = task['title']
                del self.tasks[i]
                self.save_data()
                print(f"\n✅ Tugas '{title}' berhasil dihapus!\n")
                return
        
        print(f"\n❌ Tugas dengan ID {task_id} tidak ditemukan!\n")
    
    def update_status(self, task_id, status):
        """Mengubah status tugas"""
        task = self.find_task(task_id)
        if not task:
            print(f"\n❌ Tugas dengan ID {task_id} tidak ditemukan!\n")
            return
        
        if status not in ["Selesai", "Belum Selesai"]:
            print(f"\n❌ Status harus 'Selesai' atau 'Belum Selesai'!\n")
            return
        
        task['status'] = status
        self.save_data()
        status_text = "✅ Selesai" if status == "Selesai" else "⭕ Belum Selesai"
        print(f"\n{status_text} Status tugas berhasil diperbarui!\n")
    
    def find_task(self, task_id):
        """Mencari tugas berdasarkan ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def get_statistics(self):
        """Menampilkan statistik tugas"""
        if not self.tasks:
            print("\n📊 Belum ada tugas.\n")
            return
        
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['status'] == 'Selesai')
        pending = total - completed
        
        # Statistik per kategori
        category_count = {}
        for task in self.tasks:
            cat = task['category']
            category_count[cat] = category_count.get(cat, 0) + 1
        
        print("\n" + "═"*60)
        print("📊 STATISTIK TUGAS".center(60))
        print("═"*60)
        print(f"Total Tugas          : {total}")
        print(f"✅ Selesai           : {completed}")
        print(f"⭕ Belum Selesai     : {pending}")
        print(f"Progress             : {(completed/total*100):.1f}% selesai")
        print("\n📂 Tugas per Kategori:")
        print("-"*60)
        for category, count in sorted(category_count.items()):
            bar_length = int(count / total * 30)
            bar = "█" * bar_length + "░" * (30 - bar_length)
            print(f"  {category:25} [{bar}] {count}")
        print("═"*60 + "\n")


def main_menu(todo):
    """Menampilkan menu utama"""
    while True:
        print("╔" + "═"*68 + "╗")
        print("║" + "🎯 TO-DO LIST MANAGER INTERAKTIF".center(68) + "║")
        print("╠" + "═"*68 + "╣")
        print("║ 1. 📝 Tambah Tugas Baru                                           ║")
        print("║ 2. 📋 Lihat Semua Tugas                                           ║")
        print("║ 3. ✏️  Edit Tugas                                                ║")
        print("║ 4. 🗑️  Hapus Tugas                                               ║")
        print("║ 5. ✅ Ubah Status Tugas                                           ║")
        print("║ 6. 📊 Lihat Statistik                                             ║")
        print("║ 7. 🚪 Keluar dari Program                                         ║")
        print("╚" + "═"*68 + "╝")
        
        choice = input("\nPilih menu (1-7): ").strip()
        
        if choice == '1':
            print("\n" + "─"*60)
            print("➕ TAMBAH TUGAS BARU")
            print("─"*60)
            title = input("Judul tugas: ").strip()
            if not title:
                print("❌ Judul tugas tidak boleh kosong!\n")
                input("Tekan Enter untuk melanjutkan...")
                print("\n")
                continue
            
            description = input("Deskripsi (opsional): ").strip()
            
            print("\n📂 Pilih Kategori:")
            for key, cat in CATEGORIES.items():
                print(f"   {key:2}. {cat}")
            
            category_choice = input("\nNomor kategori (1-10) [default: 1]: ").strip() or '1'
            
            category = CATEGORIES.get(category_choice, CATEGORIES['1'])
            
            todo.add_task(title, description, category)
            input("Tekan Enter untuk melanjutkan...")
        
        elif choice == '2':
            todo.view_tasks()
            input("Tekan Enter untuk melanjutkan...")
        
        elif choice == '3':
            todo.view_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang akan diedit: ").strip())
                todo.edit_task(task_id)
                input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                print("❌ ID harus berupa angka!\n")
                input("Tekan Enter untuk melanjutkan...")
        
        elif choice == '4':
            todo.view_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang akan dihapus: ").strip())
                confirm = input(f"⚠️  Yakin ingin menghapus? (y/n): ").lower()
                if confirm == 'y':
                    todo.delete_task(task_id)
                else:
                    print("❌ Penghapusan dibatalkan.\n")
                input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                print("❌ ID harus berupa angka!\n")
                input("Tekan Enter untuk melanjutkan...")
        
        elif choice == '5':
            todo.view_tasks()
            try:
                task_id = int(input("Masukkan ID tugas: ").strip())
                print("\n1. ✅ Selesai")
                print("2. ⭕ Belum Selesai")
                status_choice = input("Pilih status (1-2): ").strip()
                
                status_map = {'1': 'Selesai', '2': 'Belum Selesai'}
                if status_choice in status_map:
                    todo.update_status(task_id, status_map[status_choice])
                else:
                    print("❌ Pilihan tidak valid!\n")
                input("Tekan Enter untuk melanjutkan...")
            except ValueError:
                print("❌ ID harus berupa angka!\n")
                input("Tekan Enter untuk melanjutkan...")
        
        elif choice == '6':
            todo.get_statistics()
            input("Tekan Enter untuk melanjutkan...")
        
        elif choice == '7':
            print("\n" + "═"*60)
            print("👋 Terima kasih telah menggunakan To-Do List Manager!".center(60))
            print("Sampai jumpa lagi! 😊".center(60))
            print("═"*60 + "\n")
            break
        
        else:
            print("\n❌ Pilihan tidak valid! Silakan pilih 1-7.\n")
            input("Tekan Enter untuk melanjutkan...")
        
        print("\n")


if __name__ == "__main__":
    todo = ToDoList()
    main_menu(todo)
    I need clarification on what you'd like to add at the `$PLACEHOLDER$` location. 

    The current code is a complete to-do list application with a `main_menu()` function that's already being called in the `if __name__ == "__main__"` block.

    Could you specify what functionality you want to add? For example:
    - Additional helper functions?
    - Error handling?
    - Testing code?
    - Something else?

    Please provide more details about what "testttttt" refers to so I can help you properly.