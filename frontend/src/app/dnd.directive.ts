import { Directive, HostListener, HostBinding, EventEmitter, Output } from '@angular/core';

@Directive({
    selector: '[appDnd]',
    standalone: false
})
export class DndDirective {

  @HostBinding('class.fileover') fileOver: boolean = false;
  @Output() fileDropped = new EventEmitter<any>();

  constructor() { }



  //Dragover Listener
  @HostListener('dragover', ['$event']) onDragOver(evt:any ) {
    evt.preventDefault();
    evt.stopPropagation();
    this.fileOver = true;

    console.log('Drag Over');
  }

  //Dragleave Listener
  @HostListener('dragleave', ['$event']) public onDragLeave(evt: any) {
    evt.preventDefault();
    evt.stopPropagation();
    this.fileOver = false;

    console.log('Drag Leave');
  }

  //Drop Listener
  @HostListener('drop', ['$event']) public onDrop(evt: any) {
    if(this.fileOver) {
      evt.preventDefault();
      evt.stopPropagation();
      this.fileOver = false;
      const files = evt.dataTransfer.files;
      if(files.length > 0) {
          this.fileDropped.emit(files);
      }
    }  
  }
}
