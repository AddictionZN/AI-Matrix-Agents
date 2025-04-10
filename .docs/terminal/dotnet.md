# Dotnet CLI Commands
## Dotnet Show Help
```
dotnet --help
```

## Restore, Build, Run, Test and Show Help
```
dotnet restore
dotnet build
dotnet run
dotnet test
```

## Create a new solution
### Step 1: Create a new solution
```
mkdir <FolderName>
cd <FolderName>
dotnet new sln
```

### Step 2: Create a new console applicatio
####  Step 2.1: Create a new console application
```
dotnet new console -o <ProjectName>
```

#### Step 2.2: Add the project to the solution
```
dotnet sln add <ProjectName>/<ProjectName>.csproj
```

#### Step 2.3: Create a new class library
```
dotnet new classlib -o <ProjectName>
dotnet sln add <ProjectName>/<ProjectName>.csproj
```

#### Step 2.4: Add a reference to the class library in the console application
```
dotnet add <ProjectName>/<ProjectName>.csproj reference <ProjectName>/<ProjectName>.csproj
```

#### Step 2.5 : Build & Run Solution
```
dotnet build
dotnet run --project <ProjectName>
```

### Step 3: xUnit Test Project
#### Step 3.1: Create a new xUnit test project
```
dotnet new xunit -o <ProjectName>.Tests
dotnet sln add <ProjectName>.Tests/<ProjectName>.Tests.csproj
dotnet add <ProjectName>.Tests/<ProjectName>.Tests.csproj reference <ProjectName>/<ProjectName>.csproj
```

#### Step 3.2: Run tests in the solution
```
dotnet test
```

## Other Useful Commands
### Create a folder with a new csharp file inside
```
mkdir -p <FolderName>
touch <FolderName>/<FileName>.cs
touch <FolderName>.Tests/<FileName>.Tests.cs
```
### Add a new class to the project
```
dotnet new class -n <ClassName> -o <ProjectName>
```
### Add a new class to the test project
```
dotnet new class -n <ClassName> -o <ProjectName>.Tests
```