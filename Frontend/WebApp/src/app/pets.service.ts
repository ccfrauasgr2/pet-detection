import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, delay } from 'rxjs';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class PetsService {

  readonly APIUrl = "http://" + environment.backendIP + "/";

  constructor(private http: HttpClient) { }

  // Request one capture for a given filter
  requestCaptures(filter: any): Observable<any> {
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
    return this.http.post<any>(this.APIUrl + 'mongo/get_image', filter);
  }

}
