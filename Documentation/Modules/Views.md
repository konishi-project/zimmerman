# Views Documentation
---

These are documentations for what each endpoint does in the `views.py` module.

#### Decorators
`@jwt_required` - This means that a JSON WEB TOKEN (JWT) is required to access this route, this is usually stored in the client and used during requests.

`@limiter.limit` - This is used to reduce the amount of requests made to the server, mainly to prevent any DDoS, spam and overload the server.

*Admins usually have the power to CRUD most post this is because we don't want any automatic moderation and trusts our admins.*

Most of the decorators here are available [here](https://flask-restplus.readthedocs.io/en/stable/).

---
**Route: `/feed`**
**Class: `IdFeed`**

**Request (Get)** => Whenever the client does a get request for this route, it will return an array of post IDs e.g `[32, 82, 2, 33]` not a full post, the reason for this is that because the post might be modified or items may be added while sending full infos back to the client.

It will order the array by "latest activity" which is basically the post that has the latest comment on post or newer post. Then usually the client returns this array in a post request.

**Request (Post)** => The client is expected to send the post ID array taken from the get request, then it will get the full data for that post from the database according to the array, it also checks if the current user has liked the post and appends `liked: true or false` it thens jsonifies it and returns the info as a response.

---

**Route: `/postcomments`**
**Class: `PostComments`**

**Request (Post)** => This is very similar to the feed `post` request but it doesn't need to send any comment ID arrays since that already comes with the full post from the `/feed` endpoint.

---

**Route: `/posts`**
**Class: `NewsFeed`**

A little bit of background, this was used before feed became the main, the `get` request for this was deprecated since it can't be modified during requests like feed does.

**Request (Post)** => This route has a limit of 10 post request per day and 5 per hour. This route expects for a JSON object called `user_post` which can be found at `serializers.py`.

It'll first grab the current user's data from the database using the JWT, it will also grab the incoming JSON object, without this will trigger a `500` server error. It will then create the post `content` and `image_id` from the JSON, please null the `image_id` to prevent any issues, and if it causes a `500` error, try and force grab the JSON.

---

**Route: `/post/<int: post_id>`**
**Class: `ReadPost`**

This is used for interacting with specific post, you need to provide a `post_id` when making request from the client side URL.

**Request (Get)** => Using that `post_id` it will query the database for the Posts matching that ID. then it will return a `404` error if it's not found.. otherwise it will get the post data and checks if there is a `image_file` (This is a hashed file name that is used to get the actual image file from the server), it will add the `image_file` and returns a full jsonified post.

**Request (Post)** => This is used to add a `user_comment` to that specific post, it expects `user_comment` which can be found in `serializers.py` It will determine which post using the `post_id` being passed to it, it then grabs the JSON object, use `force=True` if it causes a 500 error on another platform, at the moment it only supports text content and no images.
**(EXPERIMENTAL)** Once it gets the comment it'll query the database for the latest one (the comment that has just been created) then it will return a JSONified full comment and success message.

**Request (Put)** => It'll get the post with the `post_id` and loads the current user's data. It will grab the JSON being sent and then updates the post's content and updates the modified date, if the post's status is locked it won't get modified and returns `403` code and message. If the user isn't the owner, it'll also return a `403` (Forbidden) code. Otherwise it'll update the post and send a `200` success code.

**Request (Delete)** => It is pretty self explanatory, it'll query the database for that specific post and deletes it from the database, it'll return `403` code if the current user does not own the post.

---

### Most of the liking system is pretty similar so I will sum it once.

**Request (Post)** => It'll load the current user and add that comment/post/reply's ID in the user's comment/post/likes which is usually an array of IDs. It'll check if the user has already liked it and returns a `403` code if they are, otherwise it'll add that and return a `200` success code.

**Request (Delete)** => It will get that specific item and removes that ID from the array of user likes then returns a `200` OK code.

---

### Most of the commenting/replying system works the same way so I will sum it once.

**Request (Get)** => Similar to specific post `get` it'll get that specific comment/reply and returns the full data of that comment/reply, if not found, it'll return a `404` error.

**Request (Post)** => It'll grab the incoming JSON object and comment/reply on that specific post, it'll first check if the post is not locked if it is, it'll return a `403` Forbidden code, otherwise it'll get the content and create that new comment/reply belonging to that post.

---

### Interacting with specific comments/replies works exactly as interacting with specific post, so I will not document that.

---

**Route: `/login`**
**Class: `UserLogin`**

**Request (Post)** => It'll expect for a `user_login` JSON object, grabs the data and if it is successful then returns an access_token that identifies the current_user, it'll validate and return error codes.

---

**Route: `/register`**
**Class: `UserRegister`**

**Request (Post)** => It'll expect for a `user_registration` JSON object, grabs the data and if it is successful it'll commit all those user information to the database and registers it, returns a `404` code if no data is found, and validates if the following credentials are available.

---

**Route: `/currentuser`**
**Class: `CurrentUser`**

**Request (Get)** => it will load the current user's data using the access token and returns the user's data back to the client.

---

**Route: `/imageupload`**
**Class: `PostImage`**

**Request (Post)** => It expects an image object file, if it doesn't exist it'll return a `404` code, if it doesn't have a name it'll return a `403` Forbidden code. Otherwise it'll check the file format to prevent any malware from affecting anything, if it passes then it'll hash that file and save it with its file format, it will then return a success message and `image_id` that the user can use for its post.