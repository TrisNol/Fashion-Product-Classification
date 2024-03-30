import { Injectable, Component } from '@angular/core';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';

@Injectable({
  providedIn: 'root'
})
export class SnackbarService {

  constructor(private snackBar: MatSnackBar ) {}

  public openSnackbar(message: string) {
    let snackBarRef = this.snackBar.open(message, "", {duration: 5000, panelClass: ['error-snack']});
  }
}
