#!/usr/bin/env python3

import re
import argparse
from ortools.sat.python import cp_model
import numpy as np

class SudokuBoard:
    def __init__(self, grid):
        row_regex = re.compile(r"\d{9}")
        assert len(grid) == 9
        for r in range(9):
            assert type(grid[r] == str) and len(grid[r]) == 9
            assert row_regex.fullmatch(grid[r])

        # conversion to 2d array of ints
        self._grid = [[int(s) for s in list(grid[r])] for r in range(9)]

    def solve(self):
        model = cp_model.CpModel()
        solver = cp_model.CpSolver()
        SudokuBoard._add_sudoku_constraints(model)
        solve_status = solver.Solve(model)
        if solve_status == cp_model.OPTIMAL:
            self.set_solution(solver)

    def set_solution(self, solver):
        for r in range(9):
            for n in range(1,10):
                value =  solver.Value()

    def _add_instance_constrains(self, model):
        #  TODO:  <18-11-20, yourname> # 
        pass

    @staticmethod
    def _add_sudoku_constraints(model):
        column_var = [
            [model.NewIntVar(0, 8, f"col_{n}_r{r}") for r in range(9)]
            for n in range(1, 10)
        ]
        for n in range(1, 10):
            model.AddAllDifferent(column_var[n])
        for r in range(9):
            model.AddAllDifferent([column_var[n][r] for n in range (1,10)])
        for i in range(3):
            for j in range(3):
                for n in range(1,10):
                    in_square_constraints = [
                        column_var[3*i+k][n] >= 3*j and column_var[3*i+k][n] < 3*(j+1) for
                        k in range(3)
                    ]
                    model.Add(sum(in_square_constraints) == 1)

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
                #  board.solve()


if __name__ == "__main__":
    main()
