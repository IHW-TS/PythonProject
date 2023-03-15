class Taquin {
    constructor(state, parent = null, move = null, g = 0) {
        this.state = state;
        this.parent = parent;
        this.move = move;
        this.g = g;
    }

    getNeighbors() {
        const neighbors = [];
        const moves = [
            ['N', [-1, 0]],
            ['S', [1, 0]],
            ['E', [0, 1]],
            ['W', [0, -1]],
        ];
        let x, y;

        for (let i = 0; i < this.state.length; i++) {
            const row = this.state[i];
            for (let j = 0; j < row.length; j++) {
                const cell = row[j];
                if (cell === 0) {
                    x = i;
                    y = j;
                    break;
                }
            }
            if (x !== undefined) {
                break;
            }
        }

        for (const [move, [dx, dy]] of moves) {
            const nx = x + dx;
            const ny = y + dy;
            if (
                nx >= 0 &&
                nx < this.state.length &&
                ny >= 0 &&
                ny < this.state[0].length
            ) {
                const newState = this.state.map((row) => row.slice());
                [newState[x][y], newState[nx][ny]] = [newState[nx][ny], newState[x][y]];
                neighbors.push(
                    new Taquin(newState, this, move, this.g + 1)
                );
            }
        }

        return neighbors;
    }

    getDistance(i, j) {
        const [targetX, targetY] = [
            Math.floor((this.state[i][j] - 1) / this.state[0].length),
            (this.state[i][j] - 1) % this.state[0].length,
        ];
        return Math.abs(targetX - i) + Math.abs(targetY - j);
    }

    h(heuristic) {
        if (heuristic === 6) {
            return this.state
                .flatMap((row, i) =>
                    row.map((cell, j) => (cell === 0 ? 0 : this.getDistance(i, j)))
                )
                .reduce((sum, dist) => sum + dist, 0);
        } else {
            const weights = [
                [36, 12, 12, 4, 1, 1, 4, 0],
                [8, 7, 6, 5, 4, 3, 2, 1],
                [8, 7, 6, 5, 3, 2, 4, 1],
            ];
            let pi;
            if (heuristic === 1) {
                pi = weights[0];
            } else if (heuristic === 2 || heuristic === 3) {
                pi = weights[1];
            } else if (heuristic === 4 || heuristic === 5) {
                pi = weights[2];
            }
            const pk =
                heuristic === 1 || heuristic === 3 || heuristic === 5 ? 4 : 1;
            return (
                this.state
                    .flatMap((row, i) =>
                        row.map(
                            (cell, j) =>
                                cell === 0 ? 0 : pi[cell - 1] * this.getDistance(i, j)
                        )
                    )
                    .reduce((sum, dist) => sum + dist, 0) // Somme des distances pondérées
            ) / pk;
        }
    }

    f(heuristic) {
        return this.g + this.h(heuristic);
    }

    compareTo(other) {
        const stateString = JSON.stringify(this.state);
        const otherStateString = JSON.stringify(other.state);
        if (stateString < otherStateString) {
            return -1;
        } else if (stateString > otherStateString) {
            return 1;
        } else {
            return 0;
        }
    }
}
function solveTaquin(initialState, finalState, heuristic) {
    const initialTaquin = new Taquin(initialState);
    const frontier = [[initialTaquin.f(heuristic), initialTaquin]];
    const explored = new Set();
    let numExplored = 0;
  
    while (frontier.length > 0) {
      frontier.sort(([f1], [f2]) => f1 - f2);
      const [_, current] = frontier.shift();
      if (JSON.stringify(current.state) === JSON.stringify(finalState)) {
        const solution = [];
        let node = current;
        while (node.parent) {
          solution.unshift(node.move);
          node = node.parent;
        }
        return [solution, numExplored];
      }
  
      explored.add(JSON.stringify(current.state));
      numExplored++;
  
      for (const neighbor of current.getNeighbors()) {
        if (!explored.has(JSON.stringify(neighbor.state))) {
          frontier.push([neighbor.f(heuristic), neighbor]);
        }
      }
    }
  
    return [null, numExplored];
  }
  
  function generateRandomState(size) {
    const state = Array.from({ length: size * size }, (_, i) => i);
    for (let i = state.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [state[i], state[j]] = [state[j], state[i]];
    }
    return Array.from({ length: size }, (_, i) =>
      state.slice(i * size, (i + 1) * size)
    );
  }
  
  function generateStates(size) {
    const initialState = generateRandomState(size);
    const finalState = Array.from({ length: size }, (_, i) =>
      Array.from({ length: size }, (_, j) => (i * size + j + 1) % (size * size))
    );
    return [initialState, finalState];
  }
  
  function printTaquin(state) {
    for (const row of state) {
      console.log(row.join(" "));
    }
    console.log();
  }
  
  const size = parseInt(prompt("Veuillez entrer la taille du taquin (par exemple, 3 pour un taquin 3x3): "));
  const [initialState, finalState] = generateStates(size);
  
  console.log("État initial du taquin :");
  printTaquin(initialState);
  
  const heuristic = parseInt(prompt("Veuillez choisir le poids à utiliser (1-6): "));
  
  const startTime = performance.now();
  const [solution, numExplored] = solveTaquin(initialState, finalState, heuristic);
  const executionTime = performance.now() - startTime;
  
  if (solution) {
    console.log(`Nombre d'états explorés: ${numExplored}`);
    console.log(`Nombre de coups joués: ${solution.length}`);
    console.log(`Solution pour heuristique h${heuristic}: ${solution.join(" ")}`);
    console.log(`Temps d'exécution: ${executionTime.toFixed(2)} millisecondes`);
    console.log(`Temps CPU: ${(performance.now() - startTime).toFixed(2)} millisecondes`);
  }
  