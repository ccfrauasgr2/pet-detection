import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { Entry } from '../entry.model';
import { PetsService } from '../pets.service';
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

  /*filter: { 
    id_filtering?: {id?: Number, filteroption?: String},
    date_filtering?: {date?: Date, filteroption?: String},
    time_filtering?: {time?: Time, filteroption?: String},
    type_filtering?: {type?: String, filteroption?: String},
    accuracy_filtering?: {accuracy?: Number, filteroption?: String, number?: String}
  } = {};*/

  filter: {
    id?: Number | null,        // From the given ID go backwards (0 means undefined)
    date?: Date | null,        // From the given Date go backwards (Either id or date will be undefined at each request)
    type?: String,      // At least one of the given type: cat/dog/all
    accuracy?: Number   // All objects on the pictures have mind. the given accuracy (0: any accuracy)
  } = {}

  show_error = false;
  show_no_more_images = false;

  constructor(private service: PetsService) { }

  ngOnChanges(changes: SimpleChanges): void {

  }

  ngOnInit(): void {
    this.apply_filter();
  }

  apply_filter() {
    this.filter.id = null;
    this.filter.date = this.date;
    this.filter.type = this.type;
    this.filter.accuracy = this.accuracy;
    this.loaded_images = [];
    this.load_images();
  }

  load_images() {
    /*// Test
    this.test_images();
    return;
    // End Test*/

    this.service.requestCaptures(this.filter).subscribe(
      res => {
        this.show_error = false;
        this.displayCaptures(res);
      },
      err => {
        this.show_error = true;
      },
      () => { }
    );
  }

  load_more() {
    /*// Test
    this.test_images();
    return;
    // End Test*/
    this.filter.id = this.lastId;
    this.filter.date = null;
    this.load_images();

  }

  displayCaptures(captures: Array<any>) {
    if (captures.length == 0) {
      this.show_no_more_images = true;
    } else {
      this.show_no_more_images = false;
      this.lastId = captures[captures.length - 1]['id'];
      this.results_to_entries(captures)
    }
  }

  results_to_entries(results: Array<any>) {
    results.forEach(element => {
      const dateTimeString = `${element['date']} ${element['time']}`;
      const [dateString, timeString] = dateTimeString.split(' ');
      const [day, month, year] = dateString.split('.');
      const [hour, minute, second] = timeString.split(':');
      const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day), parseInt(hour), parseInt(minute), parseInt(second));

      var objects: { [id: number]: [string, number] } = {}
      for (const d of element['detections']) {
        objects[d['BID']] = [d['type'], d['accuracy']];
      }
      var image = element['picture'];
      var id = element['id']
      var entry: Entry = new Entry(id, date, objects, image);
      this.loaded_images.push(entry);
    });
  }

  onBlur() {
    if (this.accuracy < 0 || this.accuracy > 100)
      this.accuracy = 0;
  }

  /*
  test_images() {
    var e1: Entry = new Entry(new Date(), { 1: ["dog", 99] }, "assets/images/shiba.jpeg");
    this.loaded_images.push(e1);
  }*/



  //Maybe delete

  /*  load_images() {
      //To implement the service
  
      this.service.readAllImages().subscribe(
        res => {
          this.result_to_entries(res);
        },
        err => { this.test = 'Observer got an error: ' + err.message },
        () => { }
      );
  
      /*var e1: Entry = new Entry(new Date(), { 1: ["dog", 99] }, "assets/images/shiba.jpeg");
      var e2: Entry = new Entry(new Date(), { 1: ["cat", 98] }, "assets/images/cat.jpeg");
      var e3: Entry = new Entry(new Date(), { 1: ["dog", 99], 2: ["cat", 95] }, "assets/images/cat_dog.jpeg");
      this.loaded_images.push(e1);
      this.loaded_images.push(e2);
      this.loaded_images.push(e3);
    }
  
    update_images() {
      //To implement the service
      var e: Entry = new Entry(new Date(), { 1: ["dog", 99], 2: ["cat", 95] }, "assets/images/cat_dog.jpeg");
      this.loaded_images.unshift(...[e]);
      this.new_captures = 0;
    }
  
    result_to_entries(result: Array<any>) {
      result.forEach(element => {
        //Convert date
        const dateTimeString = `${element['date']} ${element['time']}`;
        //const formattedDateTimeString = dateTimeString.replace(/\./g, '/');
        //const date = new Date(formattedDateTimeString);
        const [dateString, timeString] = dateTimeString.split(' ');
        const [day, month, year] = dateString.split('.');
        const [hour, minute] = timeString.split(':');
        const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day), parseInt(hour), parseInt(minute));
  
        var type = element['type'] == true ? "dog" : "cat";
        var objects: { [id: number]: [string, number] } = {
          [element['bid']]: [type, element['accuracy']]
        };
        var img = element['image']
        var entry: Entry = new Entry(date, objects, img);
        this.loaded_images.push(entry);
      });
    }*/
}
