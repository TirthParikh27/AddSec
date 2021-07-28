import React from "react";
import Button from "@material-ui/core/Button";
import CloudUploadIcon from "@material-ui/icons/CloudUpload";
import SaveIcon from "@material-ui/icons/Save";
class Main extends React.Component {
  constructor(props) {
    super(props);

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append("file", this.uploadInput.files[0]);
    data.append("filename", this.fileName.value);

    fetch("http://localhost:5000/upload", {
      method: "POST",
      body: data,
    }).then((response) => {
      if (response.status == "200") {
        console.log("Succesfully uploaded");
      }
    });
  }

  render() {
    return (
      <form onSubmit={this.handleUploadImage}>
        <div>
          <input
            ref={(ref) => {
              this.uploadInput = ref;
              this.fileName = ref;
            }}
            type="file"
          />
        </div>

        <br />

        <div>
          <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
        </div>
        <div>
        {/* <Button variant="outlined" color="primary" >
          Submit
        </Button> */}

        <Button
        type="submit"
        variant="outlined"
        color="primary"
        startIcon={<CloudUploadIcon />}
      >
        Upload
      </Button>
        </div>
      </form>
    );
  }
}

export default Main;
