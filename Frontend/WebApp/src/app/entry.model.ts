export class Entry {
    date: Date;
    objects: {[id: number] : [string, number]}
    image: string;

    constructor(date: Date, objects: {[id: number] : [string, number]}, image: string){
        this.date = date;
        this.objects = objects;
        this.image = image;
    }

}
