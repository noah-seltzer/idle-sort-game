import type { RectConfig } from "konva/lib/shapes/Rect";
import Konva from "konva";
import { get } from "svelte/store";
import { delay } from "./util/async";
const wait = (miliseconds:number) => {
    return new Promise(resolve => 
        setTimeout(() => {
            resolve(true)}, miliseconds)
        );
    } 

export interface SorterConfigProps {
    width: number;
    height: number;
    x: number;
    y: number;
    fill?: string;
    stroke?: string;
    strokeWidth?: number;
    draggable?: boolean;
}

const MAX_ARRAY_DEFAULT = 100;

export class Sorter {
    private _obj: Konva.Group;
    private arrayLen = 10;
    private array: number[] = [];
    private delay = 100;
    private maxArrayValue = MAX_ARRAY_DEFAULT;
    private rects: Konva.Rect[] = [];
    constructor(private config: SorterConfigProps, private layer: Konva.Layer) {
        this._obj = new Konva.Group(this.config);
        const background = new Konva.Rect({
            x: 0,
            y: 0,
            width: this.config.width,
            height: this.config.height,
            stroke: "black",
            strokeWidth: 5,
        })
        // const background = new Konva.Rect(this.config);
        this._obj.add(background);
        this.generateRandomArray();
        this.drawArray([], true).then(() => {
            this.sortArray()
        });

    }

    generateRandomArray(){
        this.array = new Array(this.arrayLen).fill(0).map(() => Math.floor(Math.random() * this.maxArrayValue))
    }

    clear() {
        this.rects.forEach(rect => rect.destroy());
        this.rects = [];
    }

    async drawArray(highlightedIndices: number[] = [], delay = false) {
        this.clear();
        const { width: containerWidth, height: containerHeight } = this.config;
        const barWidth = containerWidth / this.arrayLen;

        const paddedHeight = containerHeight * 0.95

        for (let i = 0; i < this.array.length; i++) {
            const item = this.array[i];
            const barHeight = paddedHeight * (item / this.maxArrayValue);
            const x = i * barWidth + 1
            const y = containerHeight - barHeight
            const rect = new Konva.Rect({
                x,
                y,
                width: barWidth,
                height: barHeight,
                fill: highlightedIndices.includes(i) ? "red" : "blue",   });
            this._obj.add(rect);
            this.rects.push(rect);
            if (delay) {
                await wait(this.delay);
            }
        }
    }
    swap(i: number, j:number) {
        [this.array[i], this.array[j]] = [this.array[j], this.array[i]]; // Use array destructuring for swap
    }
    async sortArray() {
            // No need for local copy if main loop manages it
            for (let i = 0; i < this.array.length; i++) {
                for (let j = 0; j < this.array.length - i - 1; j++) {
                    if (this.array[j] > this.array[j + 1]) {
                        this.swap(j, j + 1);
                        await this.drawArray([j, j + 1]); // Use helper
                    } else {
                        // Optional: Visualize comparison even if no swap
                        await this.drawArray([j, j + 1]);
                    }
                }
                await wait(this.delay); // Optional: Delay after each outer loop iteration
            }
    }

    get obj() {
        return this._obj;
    }
}