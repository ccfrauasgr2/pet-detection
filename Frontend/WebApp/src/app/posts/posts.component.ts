import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { Entry } from '../entry.model';
import { PetsService } from '../pets.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Time } from '@angular/common';

@Component({
  selector: 'app-posts',
  templateUrl: './posts.component.html',
  styleUrls: ['./posts.component.css']
})
export class PostsComponent implements OnInit, OnChanges {

  type = "all"
  date = new Date();
  accuracy = 0;
  maxDate = new Date();
  loaded_images: Entry[] = [];
  new_captures: number = 0;
  lastId: any;

  counter = 0;


  filter: {
    id?: Number | null,         // From the given ID go backwards (0 means undefined)
    date?: String | null,       // From the given Date go backwards (Either id or date will be undefined at each request)
    type?: String,              // At least one of the given type: cat/dog/all
    accuracy?: Number           // All objects on the pictures have mind. the given accuracy (0: any accuracy)
  } = {}

  show_error = false;
  show_no_more_images = false;




  constructor(private service: PetsService) { }

  ngOnChanges(changes: SimpleChanges): void {

  }

  ngOnInit(): void {
    this.apply_filter();
  }


  // Apply the filter and load the images
  apply_filter() {
    this.filter.id = null;
    this.filter.date = this.date_to_str();
    this.filter.type = this.type;
    this.filter.accuracy = this.accuracy / 100;
    this.loaded_images = [];

    this.load_images();

  }

  // Load images from backend
  load_images() {
    if (this.filter['id']?.valueOf() != undefined) {
      if (this.filter['id'].valueOf() < 2) {
        this.show_no_more_images = true;
        this.counter = 0;
        return;
      }
    }

    this.service.requestCaptures(this.filter).subscribe(
      res => {
        this.show_error = false;
        this.show_no_more_images = false;
        this.displayCapture(res);
        if (this.counter == 9) {
          this.counter = 0;
          return
        }
        else {
          this.counter++;
          this.load_more()
        }

      },
      (err: HttpErrorResponse) => {
        this.counter = 0
        if (err.status === 424) {
          this.show_no_more_images = true;
        }

        else {
          this.show_error = true;
        }

      },
      () => { }
    );
  }

  // Load next image
  load_more() {
    this.filter.id = this.lastId;
    this.filter.date = null;
    this.load_images();

  }

  // Convert received capture JSON to Entry object and add to list
  displayCapture(capture: any) {
    this.lastId = capture['id'] - 1;

    //Capture JSON to Entry object
    const dateTimeString = `${capture['date']} ${capture['time']}`;
    const [dateString, timeString] = dateTimeString.split(' ');
    const [year, month, day] = dateString.split('-');
    const [hour, minute, second] = timeString.split(':');
    const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day), parseInt(hour), parseInt(minute), parseInt(second));

    var objects: { [id: number]: [string, number] } = {}
    for (const d of capture['detections']) {
      objects[d['bid']] = [d['type'], d['accuracy']];
    }

    var image = "data:image/jpeg;base64," + capture['picture'];
    var id = capture['id']
    var entry: Entry = new Entry(id, date, objects, image);
    this.loaded_images.push(entry);
  }

  // Allow accuracy only between 0 and 100
  onBlur() {
    if (this.accuracy < 0 || this.accuracy > 100)
      this.accuracy = 0;
  }


  // Converting the selected date to string
  date_to_str() {

    var year = this.date.getFullYear();
    var month = this.date.getMonth();
    var day = this.date.getDate();
    var month_str = "";
    var day_str = "";
    if (month != undefined) {
      month += 1;
      month_str = month < 10 ? "0" + month : "" + month;
    }
    if (day != undefined) {
      day_str = day < 10 ? "0" + day : "" + day;
    }
    var date: string = "" + year + "-" + month_str + "-" + day_str;

    return date;
  }

}
