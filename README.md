#VENV

create venv first for python, usage: python3 -m venv ```<foldername>``` then

cd ```<foldername>``` and then git clone in venv

#All models for users are in ```Models``` and for admin are in ```ModelsAdmin```


#All controllers are in ```Controllers```  and for admin controllers are in ```ControllersAdmin```

then proccess from controllers in ```ViewSets``` and register it to ```AdminPages``` & ```Routers```

for workflow this project

1.registering all models in `Models`
2.from models to `Controllers->serializers.py`
3.from `serializers` then used it in `Controllers->views.py`
4.and then registering that class name in views to `Routers->urls.py` for accessible in browser, include method e.g: `get : get`, `post : post`, `put : update`, `delete : delete`