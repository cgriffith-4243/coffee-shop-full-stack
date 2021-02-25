# Coffee Shop Full Stack

## Coffee Shop

Coffee Shop is a web application for managing drink menu items and recipes. The application can:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

## Documentation

README documentation for the Frontend and Backend of this application:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

## Project Setup

The ./frontend directory contains the environment variables of this project, found within (./frontend/src/environment/environment.ts). These should reflect the Auth0 configuration details set up for the backend app.

## Authors

Cameron Griffith implemented the [`backend`](./backend/) for this project, authoring the [`API`](./backend/src/api.py), and integrated the [`Auth0 API`](./backend/src/auth/auth.py) into this project. Additionally, modified user [`login functionality`](./frontend/src/app/services/auth.service.ts) to work with callback url associated with the Auth0 account on this project.

The base code for this project was created by [`Udacity`](https://www.udacity.com) as part of the [`Full Stack Web Developer Nanodegree`](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) program.
