import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { Entry } from '../entry.model';
import { PetsService } from '../pets.service';
import { HttpErrorResponse } from '@angular/common/http';

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
    id?: Number | null,         // The needed ID if matching the filter, otherwise the next one
    date?: String | null,       // From the given Date go backwards (Either id or date will be null at each request)
    type?: String,              // At least one of the given type: Cat/Dog/All
    accuracy?: Number           // All objects on the pictures have mind. the given accuracy (0: any accuracy)
  } = {}

  show_error = false;
  show_no_more_images = false;
  show_add_btn = false;




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
    this.show_add_btn = false;
    this.show_error = false;
    this.show_no_more_images = false;

    if (this.filter['id']?.valueOf() != undefined) {
      if (this.filter['id'].valueOf() < 2) {
        this.show_no_more_images = true;
        this.show_add_btn = false;
        this.counter = 0;
        return;
      }
    }

    var filter_send = {
      id: this.filter.id,
      date: this.filter.date,
      type: "all",
      accuracy: 0
    }

    this.service.requestCaptures(filter_send).subscribe(
      res => {
        this.show_error = false;
        this.show_no_more_images = false;
        this.displayCapture(res);

        if (this.counter == 9) {
          this.counter = 0;
          this.show_add_btn = true;
          return
        }
        else {
          //this.counter++;
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
        this.show_add_btn = false;
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

    if (this.match_filter(entry)) {
      this.loaded_images.push(entry);
      this.counter++;
    }


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


  //Check if received image match the filter
  match_filter(entry: Entry) {

    var match_type = false;
    var match_accuracy = true;

    for (const key in entry.objects) {
      if (entry.objects[key][0] == this.filter.type || this.filter.type == "all") {
        match_type = true;
        if (this.filter.accuracy) {
          if (entry.objects[key][1] < this.filter.accuracy?.valueOf()) {
            match_accuracy = false;
          }
        }

      }

    }

    var result = match_type && match_accuracy;
    return result;

  }

}
