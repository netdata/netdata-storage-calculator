# Netdata Storage Calculator

A little [streamlit](https://streamlit.io/) based app used for estimating Netdata storage requirements.

Read Netdata documentation [here](https://learn.netdata.cloud/docs/store/change-metrics-storage).

App is available at https://netdata-storage-calculator.herokuapp.com/

You can also run the [calculator](/calculator.ipynb) notebook in google colab by pressing "Open in Colab".

## Development

Reccomended way to work on this is in a GitHub Codespace. The `.devcontainer/` folder defines what will be installed into that codespace and should have everything you need.

```bash
# run app in development mode
streamlit run app.py
```