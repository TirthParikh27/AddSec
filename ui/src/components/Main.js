import React from 'react';
import Button from "@material-ui/core/Button";
class Main extends React.Component {
  constructor(props) {
    super(props);

    

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.fileName.value);

    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      if(response.status == "200"){
        console.log("Succesfully uploaded")
      }
    });
  }

  render() {
    return (
      <form onSubmit={this.handleUploadImage}>
        <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
        </div>
        <div>
          <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
        </div>
        <br />
        <div>
        {/* <Button variant="outlined" color="primary" >
          Submit
        </Button> */}
        <button>Submit</button>
        </div>
       
      </form>
    );
  }
}

export default Main;