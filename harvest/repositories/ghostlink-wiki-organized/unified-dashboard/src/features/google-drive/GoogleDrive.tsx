import { File, Folder, Upload } from 'lucide-react'
import React from 'react'
import { Button } from '../../shared/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../shared/components/ui/card'

const GoogleDrive: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Google Drive</h1>
        <p className="text-muted-foreground">
          Manage your files and documents in Google Drive.
        </p>
      </div>

      <div className="flex space-x-4">
        <Button>
          <Upload className="h-4 w-4 mr-2" />
          Upload File
        </Button>
        <Button variant="outline">
          <Folder className="h-4 w-4 mr-2" />
          New Folder
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Files</CardTitle>
          <CardDescription>
            Your recently accessed files and folders
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center space-x-4 p-4 border rounded-lg">
              <File className="h-8 w-8 text-blue-500" />
              <div className="flex-1">
                <h3 className="font-medium">Document.pdf</h3>
                <p className="text-sm text-muted-foreground">Modified 2 hours ago</p>
              </div>
              <Button variant="ghost" size="sm">Open</Button>
            </div>
            <div className="flex items-center space-x-4 p-4 border rounded-lg">
              <Folder className="h-8 w-8 text-yellow-500" />
              <div className="flex-1">
                <h3 className="font-medium">Projects</h3>
                <p className="text-sm text-muted-foreground">12 items</p>
              </div>
              <Button variant="ghost" size="sm">Open</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default GoogleDrive