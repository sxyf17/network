document.addEventListener('DOMContentLoaded', () => {


})

function editPost(postID) {
    console.log(postID);

    textContent = document.querySelector(`#editPost-${postID}`).value;
    console.log(textContent);
    const currentTimestamp = new Date().toISOString();
    console.log(document.querySelector('#timestamp').innerHTML);


        
    fetch(`/posts/${postID}/`, {
        method: 'PUT',
        body: JSON.stringify({
            content: textContent,
            updated_at: currentTimestamp,
        })
    })

    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to update post: ${response.status}`);
        }
        console.log('Post updated successfully');
        document.querySelector('#postContent').innerHTML = `${textContent}`;
        document.querySelector('#timestamp').innerHTML = `${currentTimestamp}`;
        $('#modalEditPost' + postID).modal('hide');

    })
    .catch(error => {
        console.error('Error updating post:', error.message);
    });
    
        
}

function likePost(postID) {
    
    let updatedLikes = 0;
    // Get the post
    fetch(`/posts/${postID}`)
    .then(response => response.json())
    .then(post => {
        // Increment likes by 1
        updatedLikes = post.likes + 1;

        // Update post with new likes
        return fetch(`/posts/${postID}/`, {
            method: 'PUT',
            body: JSON.stringify({
                likes: updatedLikes,
            }),
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to update likes: ${response.status}`);
        }
        console.log('Likes updated successfully');
        console.log(`updated Likes:${updatedLikes}`);
        document.querySelector(`#likeCount-${postID}`).innerHTML = ` ${updatedLikes}`;

    })
    .catch(error => {
        console.error('Error:', error.message);
    });


}

function unlikePost(postID) {
    
    let updatedLikes = 0;
    // Get the post
    fetch(`/posts/${postID}`)
    .then(response => response.json())
    .then(post => {
        // Increment likes by 1
        updatedLikes = post.likes - 1;

        // Update post with new likes
        return fetch(`/posts/${postID}/`, {
            method: 'PUT',
            body: JSON.stringify({
                likes: updatedLikes,
            }),
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to update likes: ${response.status}`);
        }
        console.log('Likes updated successfully');
        console.log(`updated Likes:${updatedLikes}`);
        document.querySelector(`#likeCount-${postID}`).innerHTML = ` ${updatedLikes}`;

    })
    .catch(error => {
        console.error('Error:', error.message);
    });


}