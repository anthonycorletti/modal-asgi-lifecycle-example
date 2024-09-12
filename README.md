# modal-asgi-lifecycle-example

Finally! ASGI Lifecycle support on [Modal](https://modal.com).

This rather beefy example shows how you can quickly and easily create a FastAPI application on Modal that leverages the asgi lifecycle for things like request state and database sessions that connect to postgres with asyncpg.

Additionally, this code is packaged so that you can build and deploy your API in a docker container, independent of modal, incase you're selling your API to a customer that doesn't use modal... yet.
