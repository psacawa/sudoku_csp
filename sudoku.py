#!/usr/bin/env python3

import re
import argparse
from ortools.sat.python import cp_model
import numpy as np
from typing import List, cast
from functools import reduce
from operator import __and__

class SudokuBoard:
    def __init__(self, grid):
        row_regex = re.compile(r"\d{9}")
        assert len(grid) == 9
        for r in range(9):
            assert type(grid[r] == str) and len(grid[r]) == 9
            assert row_regex.fullmatch(grid[r])

        # conversion to 2d array of ints
        self._grid: List[List[int]] = [[int(s) for s in list(grid[r])] for r in range(9)]

    def solve(self):
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._add_sudoku_constraints()
        self._add_instance_constrains()
        solve_status = self._solver.Solve(self._model)
        if solve_status == cp_model.OPTIMAL:
            self.set_solution()

    def set_solution(self):
        assert self._solver, "Must be called with a solution found" 
        for r in range(9):
            for n in range(1,10):
                var = self._variables[r][n]
                c = cast(int, self._solver.Value(var))
                row = self._grid[r]
                self._grid[r][c] = n

    def _add_instance_constrains(self):
        assert self._model, "Must be called with a model created" 
        for r in range(9):
            for c in range(9):
                if self._grid[r][c] != 0:
                    n = self._grid[r][c]
                    self._model.Add(self._variables[r][n] == c)

    def _add_sudoku_constraints(self):
        assert self._model, "Must be called with a model created" 
        model = self._model
        variables = { n: [model.NewIntVar(0, 8, f"col_{n}_r{r}") for r in range(9)]
                for n in range(1, 10)
                }
        for n in range(1, 10):
            model.AddAllDifferent(variables[n])
        for r in range(9):
            model.AddAllDifferent([variables[n][r] for n in range (1,10)])
        for i in range(3):
            for j in range(3):
                for n in range(1,10):
                    in_square_constraints = [
                        variables[n][3*i+k] >= 3*j and variables[n][3*i+k] < 3*(j+1) for
                        k in range(3)
                    ]
                    #  TODO:  <18-11-20, yourname> # 
                    model.Add(not (reduce (__and__, in_square_constraints)))

        self._variables = variables

    @staticmethod
    def _print_row(row):
        return "".join ([str(k) for k in row])

    def __repr__(self):
        rows = [self._print_row(self._grid[r]) for r in range(9)]
        return "\n".join(rows)

    def __str__(self):
        return self.__repr__()


def main():
    """rozwiąż sudoku korzystając z CSP """
    parser = argparse.ArgumentParser(
        description="""
Solve a sudoku using constraint
satisfaction programming"""
    )
    parser.add_argument("--file", default="sudoku.txt")
    args = parser.parse_args()
    with open(args.file) as file:
        while True:
            header = file.readline().strip()
            if len(header) == 0:
                break
            print(header)
            if header.lower().startswith("grid"):
                grid = []
                for r in range(9):
                    grid.append(file.readline().rstrip())
                board = SudokuBoard(grid)
                print (board)
                board.solve()
                print (board)


if __name__ == "__main__":
    main()
