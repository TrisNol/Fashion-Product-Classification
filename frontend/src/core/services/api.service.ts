import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from 'src/environments/environment';
import { catchError, timeout } from 'rxjs/operators';
import { throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http:HttpClient) { }


  public getCategories(imagePath: string){
    let params: HttpParams = new HttpParams();
    params.append("path", imagePath);
    return this.http.post(environment.backend_endpoint, {path: imagePath}).pipe(timeout(5000), catchError(err => {
      return throwError(err);
    }))
  }
}
