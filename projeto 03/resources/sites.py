from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        return {'sites': site.json() for site in SiteModel.query.all()}

class Site(Resource):
    def get(self,url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'msg':'site not found'}, 404
        

    def post(self,url):
        if SiteModel.find_site(url):
            return {'msg':'this site already exists'},404
        
        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {'msg': 'An internal error ocurred trying to create a new site'}
        
        return site.json()
        

    def delete(self,url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'msg':'Site deleted'}
        return {'msg':'Site not found'},404
