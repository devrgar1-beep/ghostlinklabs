import * as d3 from 'd3';
import React, { useEffect, useRef } from 'react';
import { LatticeLink, LatticeNode, Probe, Resonance, Signal } from '../types';

interface LatticeViewProps {
  probes: Probe[];
  signals: Signal[];
  resonances: Resonance[];
  selectedTimeLayer: number;
}

const LatticeView: React.FC<LatticeViewProps> = ({
  probes,
  signals,
  resonances,
  selectedTimeLayer
}) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = 800;
    const height = 600;

    // Create nodes and links
    const nodes: LatticeNode[] = [
      ...probes.map((p, i) => ({
        id: p.id,
        type: 'probe' as const,
        x: 100,
        y: 100 + i * 80,
        data: p
      })),
      ...signals.map((s, i) => ({
        id: s.id,
        type: 'signal' as const,
        x: 300,
        y: 100 + i * 80,
        data: s
      })),
      ...resonances.map((r, i) => ({
        id: r.id,
        type: 'resonance' as const,
        x: 500,
        y: 100 + i * 80,
        data: r
      }))
    ];

    const links: LatticeLink[] = resonances.map(r => ({
      source: r.probeId,
      target: r.signalId,
      strength: r.strength
    }));

    // Create force simulation
    const simulation = d3.forceSimulation(nodes as any)
      .force('link', d3.forceLink(links as any).id((d: any) => d.id).distance(150))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('x', d3.forceX().strength(0.1))
      .force('y', d3.forceY().strength(0.1));

    // Create links
    const link = svg.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(links)
      .enter().append('line')
      .attr('stroke', '#666')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', d => Math.sqrt(d.strength) * 2);

    // Create nodes
    const node = svg.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(nodes)
      .enter().append('circle')
      .attr('r', d => d.type === 'resonance' ? 8 : 12)
      .attr('fill', d => {
        switch (d.type) {
          case 'probe': return '#4CAF50';
          case 'signal': return '#2196F3';
          case 'resonance': return '#FF9800';
          default: return '#999';
        }
      })
      .call(d3.drag<SVGCircleElement, LatticeNode>()
        .on('start', (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          (d as any).fx = d.x;
          (d as any).fy = d.y;
        })
        .on('drag', (event, d) => {
          (d as any).fx = event.x;
          (d as any).fy = event.y;
        })
        .on('end', (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          (d as any).fx = null;
          (d as any).fy = null;
        })
      );

    // Add labels
    const labels = svg.append('g')
      .attr('class', 'labels')
      .selectAll('text')
      .data(nodes)
      .enter().append('text')
      .text(d => {
        if (d.type === 'probe') return (d.data as Probe).name;
        if (d.type === 'signal') return `Signal ${(d.data as Signal).kind}`;
        return `Res ${(d.data as Resonance).strength.toFixed(2)}`;
      })
      .attr('font-size', 10)
      .attr('fill', '#fff')
      .attr('dx', 15)
      .attr('dy', 4);

    // Update positions on simulation tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);

      labels
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y);
    });

  }, [probes, signals, resonances, selectedTimeLayer]);

  return (
    <div className="lattice-view">
      <svg ref={svgRef} width="800" height="600" />
    </div>
  );
};

export default LatticeView;