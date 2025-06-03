You'll need uv 

[https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)


```bash
uv run main.py
```

# Using a camera
Change the video_source.py file and set the video_source variable to `0` to use the camera

# Video source
You can use a video file as the source by changing the `video_source.py` file and setting the `video_source` variable to the path of your video file. (example: `video_source = "path/to/video.mp4"`)

# Generated Report
When finished the report will be generated in the project root as a `patient_name.pdf` file.

# Atlas

Il faut faire la partie communication avec l'atlas.

On a mis ta fonction de requête dans `atlas.py`.

Ton modèle est utilisé dans `pain_localization.py` et il y a une fonction `timer_timeout` dans la quelle tu es censé récupérer les structures touchées à l'aide de l'atlas.

Puis dans la fonction `on_ok_clicked`, il faudrait sauvegarder les éléments dans le dictionnaire `self.pain_localization.patient_data.`

Dans `pain_localization.py`, la classe `PainLocalizationLogic` traite les images, c'est la bas que tu peux retrouver les x, y des épaules et du palpeur, tout ça quoi.