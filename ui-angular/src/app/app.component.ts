import { Component, NgZone } from '@angular/core';
import { CommonModule, DecimalPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, DecimalPipe],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  userText = '';
  result: any = null;
  loading = false;

  constructor(private zone: NgZone) {}

  async sendMessage() {
    if (!this.userText.trim()) return;

    this.loading = true;
    this.result = null;

    try {
      const res = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: this.userText })
      });
      const data = await res.json();

      // ✅ Force Angular to detect and update UI
      this.zone.run(() => {
        this.result = data;
        this.loading = false;
      });

    } catch (error) {
      this.zone.run(() => {
        this.result = { error: 'Error connecting to backend' };
        this.loading = false;
      });
    }
  }
}
