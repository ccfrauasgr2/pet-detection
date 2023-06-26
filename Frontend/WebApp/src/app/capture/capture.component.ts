import { Component, Input } from '@angular/core';
import { Entry } from '../entry.model';

@Component({
  selector: 'app-capture',
  templateUrl: './capture.component.html',
  styleUrls: ['./capture.component.css']
})
export class CaptureComponent {

  @Input() entry: Entry | undefined;

  display_date_time(date: any) {
    var sec = "" + date.getSeconds();
    if (date.getSeconds() < 10)
      sec = "0" + sec;
    return date.toLocaleString('default', { day: 'numeric', month: 'long', year: 'numeric' }) +
      " at " + date.getHours() + ":" + date.getMinutes() + ":" + sec;
  }
}