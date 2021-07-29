// import React from 'react'
// import { Grid } from '@material-ui/core'

// function ToolsConfig() {
//   const [config , setConfig] = {"CodeGuru" : "" , "ZAP" : "" , "Docker" : ""}
//   return (
//     <Grid container spacing={3}>
//       <Grid item xs={4}>

//       </Grid>

//       <Grid item xs={4}>

//       </Grid>

//       <Grid item xs={4}>

//       </Grid>

//     </Grid>
//   )
// }

// export default ToolsConfig
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
}));

export default function BasicTextFields() {
  const classes = useStyles();

  return (
    <form className={classes.root} noValidate autoComplete="off">
      <TextField id="standard-basic" label="Standard" />
      <TextField id="filled-basic" label="Filled" variant="filled" />
      <TextField id="outlined-basic" label="Outlined" variant="outlined" />
    </form>
  );
}