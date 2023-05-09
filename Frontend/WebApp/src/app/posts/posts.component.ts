import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { Entry } from '../entry.model';
import { concat } from 'rxjs';

@Component({
  selector: 'app-posts',
  templateUrl: './posts.component.html',
  styleUrls: ['./posts.component.css']
})
export class PostsComponent implements OnInit, OnChanges{

  ngOnChanges(changes: SimpleChanges): void {
    
  }

  ngOnInit(): void {
    this.load_images();
  }

  type = "all"
  date = new Date();
  maxDate = new Date();
  loaded_images: Entry[] = [];
  new_captures: number = 2;

  apply_filter(){
  
  }

  load_images(){
    //To implement the service
    var e1: Entry = new Entry(new Date(), {1:["dog", 99]}, "assets/images/shiba.jpeg");
    var e2: Entry = new Entry(new Date(), {1:["cat", 98]}, "assets/images/cat.jpeg");
    var e3: Entry = new Entry(new Date(), {1:["dog", 99], 2:["cat", 95]}, "assets/images/cat_dog.jpeg");
    this.loaded_images.push(e1);
    this.loaded_images.push(e2);
    this.loaded_images.push(e3);
  }

  update_images(){
    //To implement the service
    var e: Entry = new Entry(new Date(), {1:["dog", 99], 2:["cat", 95]}, "assets/images/cat_dog.jpeg");
    this.loaded_images.unshift(...[e]);
    this.new_captures = 0;
  }

}
