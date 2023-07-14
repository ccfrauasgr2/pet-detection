export class Entry {
    id: number;
    date: Date;
    objects: { [id: number]: [string, number] }
    image: string;

    constructor(id: number, date: Date, objects: { [id: number]: [string, number] }, image: string) {
        this.id = id;
        this.date = date;
        this.objects = objects;
        this.image = image;
    }

}
