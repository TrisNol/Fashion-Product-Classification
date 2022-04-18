import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http'
import { environment } from 'src/environments/environment';
import { catchError, timeout } from 'rxjs/operators';
import { Observable, ReplaySubject, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }


  public getCategories(imagePath: string) {
    let params: HttpParams = new HttpParams();
    params.append("path", imagePath);
    return this.http.post(environment.backend_endpoint, { path: imagePath }).pipe(timeout(5000), catchError(err => {
      return throwError(err);
    }))
  }

  convertFile(file: File): Observable<string> {
    const result = new ReplaySubject<string>(1);
    const reader = new FileReader();
    reader.readAsBinaryString(file);
    reader.onload = (event) => result.next(btoa(event.target.result.toString()));
    return result;
  }

  public categorizeImage(imageBase64: string): Observable<any> {
    return this.http.post(environment.backend_endpoint, { image: imageBase64 });
  }


}
