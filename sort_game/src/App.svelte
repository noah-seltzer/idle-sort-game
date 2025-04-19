<script lang="ts">
    import svelteLogo from './assets/svelte.svg'
    import viteLogo from '/vite.svg'
    import Counter from './components/Counter.svelte'
    import { onMount } from 'svelte'
    import { type KonvaDragTransformEvent } from 'svelte-konva'
    import Konva from 'konva'
    import type { KonvaEventListener } from 'konva/lib/Node'
import { Stage, Layer, Rect, Line } from 'svelte-konva'
    import { Sorter } from './lib/Sorter'
    const canvasWidth = 1000
    const canvasHeight = 1000
    const canvasConfig = {
        width: canvasWidth,
        height: canvasHeight,
        fill: 'white'
    }


    const generatorConfig = {
        x: 0,
        y: canvasConfig.height / 3,
        width: 250,
        height: canvasConfig.height / 3,
        fill: 'blue'
    }

    let sorterConfig = {
        x: 500,
        y: 300,
        width: 400,
        height: 200,
        fill: 'white',
        stroke: 'black',
        draggable: true
    }
    const layer = new Konva.Layer()

    const { obj: sorterRect } = new Sorter(sorterConfig, layer)

    let connectorConfig = {
        points: [
            generatorConfig.x + generatorConfig.width - 1,
            generatorConfig.y + generatorConfig.height / 2,
            sorterConfig.x + 1,
            sorterConfig.y + sorterConfig.height / 2
        ],
        stroke: 'black',
        strokeWidth: 5
      }
      const generatorRect = new Konva.Rect(generatorConfig)
      const connectorLine = new Konva.Line(connectorConfig)

      // const sorterRect = new Konva.Rect(sorterConfig)
    
    onMount(() => {
      //   // This is where you can run code when the component mounts
      //   console.log('Component mounted')
        
      const stage = new Konva.Stage({
        container: 'container',
        width: canvasWidth,
        height: canvasHeight
      })
      const backgroundRect = new Konva.Rect({
          x: 0,
        y: 0,
        width: canvasWidth,
        height: canvasHeight,
        fill: 'white'
      })
      stage.add(layer)
      layer.add(backgroundRect)
      layer.add(generatorRect)
      layer.add(connectorLine)
      layer.add(sorterRect)
      const handler = () => {
        const x = sorterRect.x() + 1
        const y = sorterRect.y() + sorterRect.height() / 2
        const oldPoints = [...connectorConfig.points]
        connectorLine.points([
          oldPoints[0],
          oldPoints[1],
          x,
          y
        ])
      }

      sorterRect.on('dragmove', handler)

    })
    // $: console.log(
    //   `Rectangle was dragged. New x: ${sorterConfig.x}. New y: ${sorterConfig.y}.`
    // );
      
      
      
    const handleSorterDrag = (sorter: KonvaDragTransformEvent) => {
      // console.log(sorter.position())
        // const x = sorterConfig.x
        // const y = sorterConfig.y + sorterConfig.height / 2
        // // sorter.
        // // // sorter.target.
        // //   // const x = sorter.target.x()
        // //   // const y = sorter.target.y()
        // //   console.log('Sorter dragged to:', x, y)
        // //   // Update the connector points
        // const oldPoints = [...connectorConfig.points]
        // connectorConfig.points = [oldPoints[0], oldPoints[1], x, y]
    }
</script>

<main>
    <div id="container"></div>
    <!-- <Stage config={{ ...canvasConfig }}>
        <Layer>
            <Rect config={canvasConfig} />
            <Rect config={generatorConfig} />
            <Line bind:config={connectorConfig} />
            <Rect bind:config={sorterConfig} on:dragmove={handleSorterDrag} />
        </Layer>
    </Stage> -->
</main>

<!-- <script lang='ts'>
  import { onMount } from 'svelte';
  // import { page } from '$app/stores';

  onMount(() => {
    
    return
    // const unsubscribe = page.subscribe((page) => {
    //   console.log('Current page:', page);
    // });

    // return () => {
    //   unsubscribe();
    // };
  });
</script> -->
<style>
    .logo {
        height: 6em;
        padding: 1.5em;
        will-change: filter;
        transition: filter 300ms;
    }
    .logo:hover {
        filter: drop-shadow(0 0 2em #646cffaa);
    }
    .logo.svelte:hover {
        filter: drop-shadow(0 0 2em #ff3e00aa);
    }
    .read-the-docs {
        color: #888;
    }
</style>
