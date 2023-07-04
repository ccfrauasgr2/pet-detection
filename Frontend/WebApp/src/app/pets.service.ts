import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class PetsService {

  //readonly APIUrl = "http://127.0.0.1:8000/"
  readonly APIUrl = "http://" + environment.backendIP + "/";

  constructor(private http: HttpClient) { }

  requestCaptures(filter: any): Observable<any> {
    const filterString = JSON.stringify(filter);
    const params = new HttpParams().set('filter', filterString);
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
    return this.http.get<any>(this.APIUrl + 'pets/get_images', { headers: headers, params: params });
  }

  checkForNewImages(id: Number): Observable<Number> {
    const params = new HttpParams().set('id', id.toString());
    return this.http.get<number>(this.APIUrl + 'pets/check_for_new_images', { params });
  }

}
