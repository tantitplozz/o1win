# ใช้ image พื้นฐานของ OpenHands Runtime
ARG ohVersion='0.40'
FROM docker.all-hands.dev/all-hands-ai/runtime:${ohVersion}-nikolaik

# ติดตั้ง dependencies พื้นฐานที่จำเป็น
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    unzip \
    vim \
    nano \
    htop \
    procps \
    sudo \
    iputils-ping \
    net-tools \
    ca-certificates \
    gnupg \
    lsb-release \
    jq \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง Node.js และ npm เวอร์ชันล่าสุด
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && npm install -g pnpm \
    && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update && apt-get install -y yarn

# ติดตั้ง Python และเครื่องมือที่เกี่ยวข้อง
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    && pip3 install --upgrade pip \
    && pip3 install pipenv poetry \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง Go
RUN curl -fsSL https://golang.org/dl/go1.21.5.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
    && echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile \
    && echo 'export PATH=$PATH:/usr/local/go/bin' >> /root/.bashrc

# ติดตั้ง Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && echo 'source $HOME/.cargo/env' >> /root/.bashrc

# ติดตั้ง Docker CLI (เพื่อให้ container สามารถใช้ Docker ของ host ได้)
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update && apt-get install -y --no-install-recommends docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf aws awscliv2.zip

# ติดตั้ง Google Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
    && apt-get update && apt-get install -y --no-install-recommends google-cloud-cli \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# ติดตั้ง Heroku CLI
RUN curl https://cli-assets.heroku.com/install.sh | sh

# ติดตั้งเครื่องมือพัฒนาเว็บ
RUN npm install -g @angular/cli \
    @vue/cli \
    create-react-app \
    gatsby-cli \
    next \
    typescript \
    eslint \
    prettier

# ติดตั้ง Java Development Kit
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง Maven และ Gradle
RUN apt-get update && apt-get install -y --no-install-recommends \
    maven \
    gradle \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง .NET SDK
RUN wget https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb -O packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update && apt-get install -y --no-install-recommends dotnet-sdk-7.0 \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง PHP และ Composer
RUN apt-get update && apt-get install -y --no-install-recommends \
    php \
    php-cli \
    php-fpm \
    php-json \
    php-common \
    php-mysql \
    php-zip \
    php-gd \
    php-mbstring \
    php-curl \
    php-xml \
    php-pear \
    php-bcmath \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้งฟอนต์ภาษาไทย
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-tlwg-laksaman \
    fonts-tlwg-laksaman-ttf \
    fonts-thai-tlwg \
    && rm -rf /var/lib/apt/lists/*

# สร้างโฟลเดอร์สำหรับเก็บเครื่องมือและสคริปต์เพิ่มเติม
RUN mkdir -p /tools

# สร้างสคริปต์เริ่มต้นที่ติดตั้งเครื่องมือที่จำเป็นสำหรับโปรเจค
RUN echo '#!/bin/bash\n\
    if [ -f "package.json" ]; then\n\
    echo "Found package.json, installing Node.js dependencies..."\n\
    npm install\n\
    fi\n\
    \n\
    if [ -f "requirements.txt" ]; then\n\
    echo "Found requirements.txt, installing Python dependencies..."\n\
    pip install -r requirements.txt\n\
    fi\n\
    \n\
    if [ -f "go.mod" ]; then\n\
    echo "Found go.mod, downloading Go dependencies..."\n\
    go mod download\n\
    fi\n\
    \n\
    if [ -f "Cargo.toml" ]; then\n\
    echo "Found Cargo.toml, installing Rust dependencies..."\n\
    cargo fetch\n\
    fi\n\
    \n\
    if [ -f "pom.xml" ]; then\n\
    echo "Found pom.xml, installing Maven dependencies..."\n\
    mvn dependency:go-offline\n\
    fi\n\
    \n\
    if [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then\n\
    echo "Found Gradle build file, installing Gradle dependencies..."\n\
    gradle dependencies\n\
    fi\n\
    \n\
    echo "Setup complete!"\n\
    ' > /tools/setup-project.sh && chmod +x /tools/setup-project.sh

# ตั้งค่า working directory และรายละเอียดเพิ่มเติม
WORKDIR /workspace
ENV PATH="/usr/local/go/bin:/root/.cargo/bin:${PATH}"
ENV LANG=th_TH.UTF-8
ENV LC_ALL=th_TH.UTF-8

# ตั้งค่า entrypoint
CMD ["/bin/bash"] 