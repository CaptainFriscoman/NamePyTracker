import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser

class ExpandedPublicSearcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Legal Public Search Tool")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        # --- Fixed Style Configuration ---
        style = ttk.Style()
        style.configure("Header.TLabel", font=("Arial", 15, "bold"))
        style.configure("Warning.TLabel", foreground="#c00000", font=("Arial", 10, "bold"))
        style.configure("Normal.TLabel", font=("Arial", 11))

        # Header
        header = ttk.Label(root, text="Public Web & Social Search", style="Header.TLabel")
        header.pack(pady=12)

        # Legal Warning
        warning_text = (
            "⚠️ LEGAL NOTICE: This tool only provides links to PUBLIC search pages. It does NOT scrape, store, or collect data.\n"
            "All searches open in your browser. You must comply with platform Terms of Service and privacy laws (GDPR, DPA 2018, etc.).\n"
            "Private or restricted content will not be accessible."
        )
        warning = ttk.Label(root, text=warning_text, style="Warning.TLabel", justify="center", wraplength=750)
        warning.pack(pady=5, padx=15)

        # Input Frame
        input_frame = ttk.Frame(root)
        input_frame.pack(pady=15, padx=25, fill="x")

        ttk.Label(input_frame, text="Full Name:", style="Normal.TLabel").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.name_entry = ttk.Entry(input_frame, width=55, font=("Arial", 11))
        self.name_entry.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(input_frame, text="Location (Optional):", style="Normal.TLabel").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.location_entry = ttk.Entry(input_frame, width=55, font=("Arial", 11))
        self.location_entry.grid(row=1, column=1, padx=8, pady=8)

        # Search Button
        search_btn = ttk.Button(input_frame, text="Search All Public Sources", command=self.run_search)
        search_btn.grid(row=2, column=0, columnspan=2, pady=18)

        # Results Area
        results_label = ttk.Label(root, text="Summary & Links:", font=("Arial", 12, "bold"))
        results_label.pack(pady=5, anchor="w", padx=25)

        self.results_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, font=("Arial", 10), width=95, height=22
        )
        self.results_area.pack(pady=5, padx=25, fill="both", expand=True)

    def run_search(self):
        self.results_area.delete("1.0", tk.END)
        name = self.name_entry.get().strip()
        location = self.location_entry.get().strip()

        if not name:
            messagebox.showwarning("Input Required", "Please enter a full name.")
            return

        # Format search terms
        query = name.replace(" ", "+")
        if location:
            query += f"+{location.replace(' ', '+')}"

        # Build summary
        summary = f"🔍 Search Summary: {name}\n"
        if location:
            summary += f"📍 Location filter: {location}\n"
        summary += "\n--- All Public Search Links ---\n\n"

        # Full list of legal public sources
        sources = [
            # General Search Engines
            {"category": "🔎 General Search Engines", "list": [
                {"name": "Google Public Search", "url": f"https://www.google.com/search?q={query}", "desc": "Full web search for public mentions."},
                {"name": "Bing Public Search", "url": f"https://www.bing.com/search?q={query}", "desc": "Alternative public web index."},
                {"name": "DuckDuckGo", "url": f"https://duckduckgo.com/?q={query}", "desc": "Privacy-focused public search."},
                {"name": "Yahoo Search", "url": f"https://search.yahoo.com/search?p={query}", "desc": "General public web results."}
            ]},
            # Social Media Public Search
            {"category": "📱 Social Media Public Search", "list": [
                {"name": "LinkedIn People Search", "url": f"https://www.linkedin.com/search/results/people/?keywords={query}", "desc": "Public professional profiles."},
                {"name": "X (Twitter) Public Search", "url": f"https://x.com/search?q={query}&src=typed_query&f=user", "desc": "Public accounts and posts."},
                {"name": "Facebook Public Search", "url": f"https://www.facebook.com/search/people/?q={query}", "desc": "Public profiles only."},
                {"name": "Instagram Public Search", "url": f"https://www.instagram.com/web/search/topsearch/?query={query}", "desc": "Public accounts preview."},
                {"name": "TikTok Public Search", "url": f"https://www.tiktok.com/search/user?q={query}", "desc": "Public creator accounts."},
                {"name": "YouTube Public Search", "url": f"https://www.youtube.com/results?search_query={query}", "desc": "Public channels and videos."},
                {"name": "GitHub Public Search", "url": f"https://github.com/search?q={query}&type=users", "desc": "Public developer profiles."}
            ]},
            # Public Directories & Records
            {"category": "📂 Public Directories & Records", "list": [
                {"name": "UK Companies House", "url": f"https://find-and-update.company-information.service.gov.uk/search/officers?q={query}", "desc": "UK public business records."},
                {"name": "OpenCorporates", "url": f"https://opencorporates.com/officers?q={query}", "desc": "Global public business records."},
                {"name": "Wikipedia", "url": f"https://en.wikipedia.org/w/index.php?search={query}", "desc": "Info on notable public figures."},
                {"name": "Whitepages", "url": f"https://www.whitepages.com/name/{name.replace(' ', '-')}", "desc": "Limited public directory listings."},
                {"name": "192.com (UK)", "url": f"https://www.192.com/people/search/?q={query}", "desc": "UK public directory data."}
            ]}
        ]

        # Add all sources to summary
        for section in sources:
            summary += f"{section['category']}\n"
            summary += "-" * 60 + "\n"
            for idx, item in enumerate(section["list"], 1):
                summary += f"{idx}. {item['name']}\n"
                summary += f"   • {item['desc']}\n"
                summary += f"   • Link: {item['url']}\n\n"

        summary += "--- Important Notes ---\n"
        summary += "• Click any blue link to open it in your browser.\n"
        summary += "• Results only show what is set to PUBLIC.\n"
        summary += "• Private profiles, addresses, or phone numbers will not appear.\n"
        summary += "• Do not misuse results for harassment or unlawful purposes.\n"

        self.results_area.insert(tk.END, summary)

        # Make all links clickable
        self.make_links_clickable(sources)

    def make_links_clickable(self, sources):
        for section in sources:
            for item in section["list"]:
                url = item["url"]
                start = self.results_area.search(url, "1.0", tk.END)
                if start:
                    end = f"{start}+{len(url)}c"
                    self.results_area.tag_add(url, start, end)
                    self.results_area.tag_config(url, foreground="#0033cc", underline=1)
                    self.results_area.tag_bind(url, "<Button-1>", lambda e, u=url: webbrowser.open(u))

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpandedPublicSearcher(root)
    root.mainloop()